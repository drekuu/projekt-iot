from sqlite3 import connect, OperationalError, IntegrityError
attributes: dict[str, str] = {
    'Courses': '(CourseID, CourseName)',
    'Stops': '(StopID, StopName)',
    'Assignments': '(CourseID, StopID, StopNumber)',
    'Workers': '(WorkerID, WorkerFirstName, WorkerLastName, WorkerBalance, WorkerCardID)',
    'Buses': '(BusID, CourseID, StopNumber)',
    'CurrentRides': '(RideID, WorkerCardID, BusID, StopsTraveled)'
}


def connect_to_db() -> tuple:
    connection = connect(f'alpha.db')
    return connection, connection.cursor()


def disconnect_from_db(connection, cursor) -> None:
    connection.commit()
    cursor.close()
    connection.close()


def init_db() -> None:
    connection, cursor = connect_to_db()
    try:
        with open(f'init.sql', 'r') as sql_file:
            cursor.executescript(sql_file.read())
    except OperationalError:
        print("Baza danych już istnieje. Nie podjęto inicjalizacji.")
    finally:
        disconnect_from_db(connection, cursor)


def insert_example() -> None:
    connection, cursor = connect_to_db()
    with open(f'insert_example.sql', 'r') as sql_file:
        cursor.executescript(sql_file.read())
    disconnect_from_db(connection, cursor)


def names_of_attributes_to_string(names_of_attributes: list[str]):
    result = ''
    for name in names_of_attributes:
        result += f'{name},'
    return result[:-1]


def where_statements_to_string(where_statements: list[tuple]):
    result = ''
    for where_statement in where_statements:
        result += f'{where_statement[0]} = {parse_to_sql(where_statement[1])} AND '
    return result[:-5]


def select(table_name: str, names_of_attributes_to_select: list[str], where_statements: list[tuple]) -> list:
    connection, cursor = connect_to_db()
    attributes = names_of_attributes_to_string(names_of_attributes_to_select)
    cursor.execute(f"SELECT {attributes} FROM {table_name} "
                   f"WHERE {where_statements_to_string(where_statements)};")
    cursor_result = cursor.fetchall()
    disconnect_from_db(connection, cursor)
    return cursor_result


def select_all(table_name: str, names_of_attributes_to_select: list[str]) -> list:
    connection, cursor = connect_to_db()
    attributes = names_of_attributes_to_string(names_of_attributes_to_select)
    cursor.execute(f"SELECT {attributes} FROM {table_name};")
    cursor_result = cursor.fetchall()
    disconnect_from_db(connection, cursor)
    return cursor_result


def insert(table_name: str, tuple_to_insert: tuple):
    connection, cursor = connect_to_db()
    try:
        cursor.execute(f"INSERT INTO {table_name} {attributes[table_name]} VALUES {tuple_to_insert};")
    except IntegrityError:
        raise IntegrityError
    finally:
        disconnect_from_db(connection, cursor)


def delete(table_name: str, where_attribute: tuple):
    parsed_where_value = parse_to_sql(where_attribute[1])
    connection, cursor = connect_to_db()
    if table_name == 'Courses':
        course_id = select('Courses', 'CourseID', where_attribute)
        delete('Assignments', ('CourseID', course_id))
    elif table_name == 'Stops':
        stop_id = select('Stops', 'StopID', where_attribute)
        delete('Assignments', ('StopID', stop_id))
    cursor.execute(f"DELETE FROM {table_name} WHERE {where_attribute[0]} = {parsed_where_value};")
    disconnect_from_db(connection, cursor)


def update(table_name: str, set_attribute: tuple, where_attribute: tuple):
    connection, cursor = connect_to_db()
    parsed_set_value = parse_to_sql(set_attribute[1])
    parsed_where_value = parse_to_sql(where_attribute[1])
    cursor.execute(f"UPDATE {table_name} SET {set_attribute[0]} = {parsed_set_value}"
                   f" WHERE {where_attribute[0]} = {parsed_where_value};")
    disconnect_from_db(connection, cursor)


def parse_to_sql(value):
    return f"'{value}'" if (type(value) == str and value != 'null') else value


def print_db():
    connection, cursor = connect_to_db()
    for table_name in ['Courses', 'Stops', 'Assignments', 'Workers', 'Buses', 'CurrentRides']:
        print('- - - - - - - - - - - - - - - - -')
        print(table_name)
        cursor.execute(f"SELECT * FROM {table_name};")
        for row in cursor.fetchall():
            print(row)
    disconnect_from_db(connection, cursor)


if __name__ == '__main__':
    # init_db()
    # insert_example()
    print_db()
