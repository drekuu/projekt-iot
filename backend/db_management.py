from sqlite3 import connect, OperationalError, IntegrityError
attributes: dict[str, str] = {
    'Courses': '(CourseID, CourseName)',
    'Stops': '(StopID, StopName)',
    'Assignments': '(CourseID, StopID, StopNumber)',
    'Workers': '(WorkerID, WorkerFirstName, WorkerLastName, WorkerBalance, WorkerCardID)',
    'CurrentRides': '(RideID, WorkerID, StopsTraveled)'
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


def select(table_name: str, name_of_attribute_to_select: str, where_attribute: tuple) -> list:
    connection, cursor = connect_to_db()
    parsed_where_value = parse_to_sql(where_attribute[1])
    cursor.execute(f"SELECT {name_of_attribute_to_select} FROM {table_name} "
                   f"WHERE {where_attribute[0]} = {parsed_where_value};")
    cursor_result = cursor.fetchall()
    disconnect_from_db(connection, cursor)
    return [tup[0] for tup in cursor_result]


def select_all(table_name: str, name_of_attribute_to_select: str) -> list:
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT {name_of_attribute_to_select} FROM {table_name};")
    cursor_result = cursor.fetchall()
    disconnect_from_db(connection, cursor)
    return [tup[0] for tup in cursor_result]


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
    for table_name in ['Courses', 'Stops', 'Assignments', 'Workers', 'CurrentRides']:
        print('- - - - - - - - - - - - - - - - -')
        print(table_name)
        cursor.execute(f"SELECT * FROM {table_name};")
        for row in cursor.fetchall():
            print(row)
    disconnect_from_db(connection, cursor)


if __name__ == '__main__':
    # init_db()
    print_db()
