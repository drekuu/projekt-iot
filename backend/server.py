import uvicorn
from fastapi import FastAPI
import db_management
from sqlite3 import OperationalError

app = FastAPI()


# --- INFO ENDPOINTS ---

@app.get("/courses")
async def courses_endpoint():
    result = {}
    courses = db_management.select_all('Courses', ['CourseID', 'courseName'])
    for course_id, course_name in courses:
        stops = db_management.select('Assignments', ['StopID', 'StopNumber'], [('CourseID', course_id)])
        result[course_name] = ['' for _ in range(len(stops))]
        for stop_id, stop_number in stops:
            stop_name = db_management.select('Stops', ['StopName'], [('StopID', stop_id)])[0][0]
            result[course_name][stop_number-1] = stop_name
    return result


@app.get("/workers")
async def workers_endpoint():
    workers_data = db_management.select_all('Workers', ['WorkerID', 'WorkerFirstName', 'WorkerLastName',
                                                        'WorkerBalance', 'WorkerCardID'])
    result = {}
    for worker_id, first_name, last_name, balance, card_id in workers_data:
        result[worker_id] = {
            'first_name': first_name,
            'last_name': last_name,
            'balance': balance,
            'card_id': card_id
            }
    return result


@app.get("/buses")
async def buses_endpoint():
    buses_data = db_management.select_all('Buses', ['BusID', 'CourseID', 'StopsInAscendingOrder', 'StopNumber'])
    result = {}
    for bus_id, course_id, stops_order, stop_number in buses_data:
        if not course_id:
            result[bus_id] = {}
        else:
            course_name = db_management.select('Courses', ['CourseName'], [('CourseID', course_id)])[0][0]
            stop_number = stop_number
            direction = 'right' if stops_order else 'left'
            result[bus_id] = {
                'course_name': course_name,
                'stop_number': stop_number,
                'direction': direction
            }
    return result


# --- ACTION ENDPOINTS ---

NEXT_STOP = 0
ROUTE_ENDED = 1
NO_SUCH_BUS = 2
BUS_NOT_ON_ROUTE = 3

@app.get("/nextstop/{bus_id}")
async def next_stop_endpoint(bus_id: int) -> dict[str, str]:
    result_code = next_stop(bus_id)
    if result_code == ROUTE_ENDED:
        return {'success': 'The route has ended.'}
    elif result_code == NO_SUCH_BUS:
        return {'error': f'No bus with ID {bus_id}.'}
    elif result_code == BUS_NOT_ON_ROUTE:
        return {'error': 'The bus is not on any route.'}
    else:
        return result_code

@app.get("/choosecourse/{bus}")
async def choose_course_endpoint(bus: int, course: str, direction: bool):
    """
    :param bus: Bus ID
    :param course: Course name
    :param direction: true if beginning from the first stop of the course, false if from the last one
    """
    choose_course(bus, course, direction)
    return {'success': f'The course of bus with ID {bus} is now {course}. It starts from the '
                       f'{"first" if direction else "last"} stop of the route.'}


## --- OTHER METHODS ---


## --- MQTT COMMUNICATION ---

def next_stop(bus_id: int)
    bus_data = db_management.select('Buses', ['BusID', 'CourseID', 'StopsInAscendingOrder', 'StopNumber'],
                                    [('BusID', bus_id)])
    if not bus_data:
        return NO_SUCH_BUS
    bus_id, course_id, stops_order, stop_number = bus_data[0]
    try:
        stops = [tup[0] for tup in db_management.select('Assignments', ['StopID'],
                                                        [('CourseID', course_id)])]
    except OperationalError:
        return BUS_NOT_ON_ROUTE
    if stops_order == 1:
        new_stop_number = stop_number + 1
        new_stop_number_to_display = new_stop_number
    else:
        new_stop_number = stop_number - 1
        new_stop_number_to_display = len(stops) - new_stop_number
    if new_stop_number == 0 or new_stop_number > len(stops):
        for attribute_name in ['CourseID', 'StopsInAscendingOrder', 'StopNumber']:
            db_management.update('Buses', (attribute_name, 'null'), ('BusID', bus_id))
        return ROUTE_ENDED
    else:
        db_management.update('Buses', ('stopNumber', new_stop_number), ('BusID', bus_id))
        new_stop_id = db_management.select('Assignments', ['StopID'],
                                           [('CourseID', course_id), ('stopNumber', new_stop_number)])[0][0]
        new_stop_name = db_management.select('Stops', ['StopName'], [('StopID', new_stop_id)])[0][0]
        return {'success': f'{new_stop_number_to_display}. {new_stop_name}'}

def choose_course(bus_id: int, course_name: str, direction: bool):
    course_id = db_management.select('Courses', ['CourseID'], [('CourseName', course_name)])[0][0]
    db_management.update('Buses', ('CourseID', course_id), ('BusID', bus_id))
    db_management.update('Buses', ('StopsInAscendingOrder', int(direction)), ('BusID', bus_id))
    if direction:
        stop_number = 1
    else:
        stop_number = len(db_management.select('Assignments', ['CourseID'], [('CourseID', course_id)]))
    db_management.update('Buses', ('StopNumber', stop_number), ('BusID', bus_id))


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=55555)
