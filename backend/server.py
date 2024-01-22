import uvicorn
from fastapi import FastAPI
import db_management
from mqtt_server import run_mqtt_server

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
    buses_data = db_management.select_all('Buses', ['BusID', 'CourseID', 'StopNumber'])
    result = {}
    for bus_id, course_id, stop_number in buses_data:
        if not course_id:
            result[bus_id] = {}
        else:
            course_name = db_management.select('Courses', ['CourseName'], [('CourseID', course_id)])[0][0]
            result[bus_id] = {
                'course_name': course_name,
                'stop_number': stop_number
            }
    return result


@app.get("/stops")
async def stops_endpoint():
    stops_data = db_management.select_all('Stops', ['StopID', 'StopName'])
    result = {}
    for stop_id, stop_name in stops_data:
        result[stop_id] = stop_name
    return result


# --- ACTION ENDPOINTS ---


@app.get("/addbalance/{worker_id}")
async def add_balance_endpoint(worker_id: int, value: float):
    current_balance = db_management.select('Workers', ['WorkerBalance'], [('WorkerID', worker_id)])[0][0]
    db_management.update('Workers', ('WorkerBalance', current_balance + value), ('WorkerID', worker_id))
    return {'success': f'Balance of worker with ID {worker_id} has changed from {current_balance} to '
                       f'{current_balance + value}'}


@app.get("/addworker")
async def add_worker_endpoint(firstname: str, lastname: str, card: str):
    max_id = max([tup[0] for tup in db_management.select_all('Workers', ['WorkerID'])])
    db_management.insert('Workers', (max_id + 1, firstname, lastname, 0.0, card))
    return {'success': f'Worker {firstname} {lastname} added successfully.'}


@app.get("/addcourse/{course_name}/{stops}")
async def add_course_endpoint(course_name: str, stops: str):
    max_id = max([tup[0] for tup in db_management.select_all('Courses', ['CourseID'])])
    db_management.insert('Courses', (max_id + 1, course_name))
    stops = stops.split(',')
    for stop_number, stop in enumerate(stops):
        db_management.insert('Assignments', (max_id + 1, stop, stop_number + 1))
    return {'success': f'Course {course_name} added successfully.'}


@app.get("/addstop/{stop_name}")
async def add_stop_endpoint(stop_name: str):
    max_id = max([tup[0] for tup in db_management.select_all('Stops', ['StopID'])])
    db_management.insert('Stops', (max_id + 1, stop_name))
    return {'success': f'Stop {stop_name} added successfully.'}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5555)
    run_mqtt_server()
