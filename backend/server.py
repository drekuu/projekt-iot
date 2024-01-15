import uvicorn
from fastapi import FastAPI
import db_management

app = FastAPI()

@app.get("/courses")
async def courses():
    result = {}
    courses = db_management.select_all('Courses', ['CourseID', 'courseName'])
    for course_id, course_name in courses:
        stops = db_management.select('Assignments', ['StopID', 'StopNumber'], ('CourseID', course_id))
        result[course_name] = ['' for _ in range(len(stops))]
        for stop_id, stop_number in stops:
            stop_name = db_management.select('Stops', ['StopName'], ('StopID', stop_id))[0][0]
            result[course_name][stop_number-1] = stop_name
    return result


@app.get("/workers")
async def health():
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
    
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=55555)