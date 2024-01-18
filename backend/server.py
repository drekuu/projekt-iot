import uvicorn
from fastapi import FastAPI
import db_management
from sqlite3 import OperationalError

app = FastAPI()


# --- INFO ENDPOINTS ---

@app.get("/courses")
async def courses():
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
async def workers():
    workers_data = db_management.select_all('Workers', ['WorkerID', 'WorkerFirstName', 'WorkerLastName', 'WorkerBalance', 'WorkerCardID'])
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
async def buses():
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

@app.get("/nextstop/{bus_id}")
async def next_stop(bus_id: int):
    bus_data = db_management.select('Buses', ['BusID', 'CourseID', 'StopsInAscendingOrder', 'StopNumber'],
                                    [('BusID', bus_id)])
    if not bus_data:
        return {'error': f'No bus with ID {bus_id}.'}
    bus_id, course_id, stops_order, stop_number = bus_data[0]
    try:
        stops = [tup[0] for tup in db_management.select('Assignments', ['StopID'],
                                                        [('CourseID', course_id)])]
    except OperationalError:
        return {'error': 'The bus is not on any route.'}
    if stops_order == 1:
        new_stop_number = stop_number + 1
        new_stop_number_to_display = new_stop_number
    else:
        new_stop_number = stop_number - 1
        new_stop_number_to_display = len(stops) - new_stop_number
    if new_stop_number == 0 or new_stop_number > len(stops):
        for attribute_name in ['CourseID', 'StopsInAscendingOrder', 'StopNumber']:
            db_management.update('Buses', (attribute_name, 'null'), ('BusID', bus_id))
        return {'success': 'The route has ended.'}
    else:
        db_management.update('Buses', ('stopNumber', new_stop_number), ('BusID', bus_id))
        new_stop_id = db_management.select('Assignments', ['StopID'],
                                           [('CourseID', course_id), ('stopNumber', new_stop_number)])[0][0]
        new_stop_name = db_management.select('Stops', ['StopName'], [('StopID', new_stop_id)])[0][0]
        return {'success': f'{new_stop_number_to_display}. {new_stop_name}'}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=55555)
