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

### /stops
    {  
        <stop_id>(string): <stop_name>(string),
        ...
    }

## Action endpoints

### /addbalance/<worker_id>
Query parameters:
* value - Money to add

Example:

    /addbalance/6?value=20.0

Response:

    {"success":"Balance of worker with ID 6 has changed from 800.0 to 820.0"}

### /addworker
Query parameters:
* firstname - First name
* lastname - First name
* card - Card ID

Example:

    /addworker?firstname=Adam&lastname=Sandlers&card=W9999

Response:

    {"success":"Worker Adam Sandlers added successfully."}

### /addCourse/<course_name>
Query parameters:
* stops - Stops as stop1,stop2,...,stopN

Example:

    /addcourse/NewCourse?stops=1,3,5,6

Response:

    {"success":"Course NewCourse added successfully."}

### /addStop/<stop_name>

Example:

    /addstop/NewStop

Response:

    {"success":"Stop NewStop added successfully."}