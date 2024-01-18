# REST API endpoints
port - 55555

## Info endpoints

### /courses
    {
        <course_name>(string): <stops_names>(list of strings),
        ...
    }

### /workers
    {
        <worker_id>(string): {
            "first_name": <first_name>(string),
            "last_name": <last_name>(string),
            "balance": <balance>(float),
            "card_id": <card_id>(string)
        },
        ...
    }

### /buses
    {  
        <bus_id>(string): {     //bus on the route
            "course_name": <course_name>(string),
            "stop_number": <stop_number>(int),
            "direction": "left" or "right"
        },
        <bus_id>(string): {},   //bus not on the route
        ...
    }

## Action endpoints

### /nextstop/<bus_id>
if bus is on the route, and it's not his last stop:

    {
        "success": "<new_stop_number>. <new_stop_name>"
    }

if bus is on the route, and it's his last stop:

    {
        "success": "The route has ended."
    }

if the bus is not on the route:

    {
        "error": "The bus is not on any route."
    }

if there is no bus with provided id:

    {
        "error": "No bus with ID <provided_bus_id>."
    }

### /choosecourse
Proper request should include query parameters:
* bus - Bus ID
* course - Course ID
* direction - true if beginning from the first stop of the course, false if from the last one

Example:

    /choosecourse?bus=4&course=LongCourse&direction=false

Response:

    {"success":"The course of bus with ID 4 is now LongCourse. It starts from the last stop of the route."}