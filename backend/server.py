import uvicorn
from fastapi import FastAPI
import db_management
from sqlite3 import OperationalError

app = FastAPI()


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


@app.get("/nextstop/{bus_id}")
async def next_stop(bus_id: int):
    try:
        bus_data = db_management.select('Buses', ['CourseID', 'StopsInAscendingOrder', 'StopNumber'], [('BusID', bus_id)])
    except OperationalError:
        return {'error': f'No bus with ID {bus_id}.'}
    course_id, stops_order, stop_number = bus_data[0]
    stops = [tup[0] for tup in db_management.select('Assignments', ['StopID'], [('CourseID', course_id)])]


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=55555)
