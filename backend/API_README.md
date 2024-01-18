# REST API endpoints
port - 55555

## Info endpoints

### /courses

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

