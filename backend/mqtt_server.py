import paho.mqtt.client as mqtt
import db_management
from sqlite3 import OperationalError

broker_ip = "0.0.0.0"

CLIENT = mqtt.Client()


def query_string_to_dict(query_string):
    key = query_string.split('?')[0]
    values = query_string.split('?')[1].split('&')
    result_dict = {}
    values_dict = {}
    for value in values:
        values_dict[value.split('=')[0]] = value.split('=')[1]
    result_dict[key] = values_dict
    return result_dict


NEXT_STOP = 0
ROUTE_ENDED = 1
NO_SUCH_BUS = 2
BUS_NOT_ON_ROUTE = 3


def process_message(client, userdata, message):
    global CLIENT
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")[0]
    message_dict = query_string_to_dict(message_decoded)
    if 'next_stop' in message_dict:
        result_code = next_stop(message_dict['next_stop']['bus'])
        if result_code == ROUTE_ENDED:
            CLIENT.publish('response/success', 'end')
        elif result_code == NO_SUCH_BUS:
            CLIENT.publish('response/error', f'no bus')
        elif result_code == BUS_NOT_ON_ROUTE:
            CLIENT.publish('response/error', 'no route')
        else:
            CLIENT.publish('response/success', result_code)
    elif 'choose_course' in message_dict:
        choose_course(message_dict['choose_course']['bus'], message_dict['choose_course']['course'],
                      bool(int(message_dict['choose_course']['direction'])))
        course_id = db_management.select('Courses', ['CourseID'], [('CourseName',
                                                                    message_dict['choose_course']['course'])])[0][0]
        if int(message_dict['choose_course']['direction']):
            stop_number = 1
        else:
            stop_number = len(db_management.select('Assignments', ['StopID'], [('CourseID', course_id)]))
        stop_id = db_management.select('Assignments', ['StopID'], [('CourseID', course_id),
                                                                   ('StopNumber', stop_number)])[0][0]
        stop_name = db_management.select('Stops', ['StopName'], [('StopID', stop_id)])[0][0]
        CLIENT.publish('response/success', f'1-{stop_name}')
    elif 'use_card' in message_dict:
        result_code = card_used(message_dict['use_card']['card'], message_dict['use_card']['bus'])
        CLIENT.publish('response/success', result_code)


def connect_to_broker():
    CLIENT.connect(broker_ip)
    CLIENT.on_message = process_message
    CLIENT.loop_start()
    CLIENT.subscribe("buses/#")


def disconnect_from_broker():
    CLIENT.loop_stop()
    CLIENT.disconnect()


def run_mqtt_server():
    connect_to_broker()
    input()


def next_stop(bus_id: int):
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
        return f'{new_stop_number_to_display}-{new_stop_name}'


def choose_course(bus_id: int, course_name: str, direction: bool):
    course_id = db_management.select('Courses', ['CourseID'], [('CourseName', course_name)])[0][0]
    db_management.update('Buses', ('CourseID', course_id), ('BusID', bus_id))
    db_management.update('Buses', ('StopsInAscendingOrder', int(direction)), ('BusID', bus_id))
    if direction:
        stop_number = 1
    else:
        stop_number = len(db_management.select('Assignments', ['CourseID'], [('CourseID', course_id)]))
    db_management.update('Buses', ('StopNumber', stop_number), ('BusID', bus_id))


def add_stop_to_workers(bus_id: int):
    workers_in_the_bus = [tup[0] for tup in db_management.select('CurrentRides', ['WorkerID', 'StopsTraveled'],
                                                                 [('BusID', bus_id)])]
    for worker_id, stops_traveled_already in workers_in_the_bus:
        db_management.update('CurrentRides', ('StopsTraveled', stops_traveled_already + 1), ('BusID', bus_id))


def card_used(card_id: str, bus_id: int):
    worker_id = db_management.select('Workers', ['WorkerID'], [('WorkerCardID', card_id)])[0][0]
    riding_workers = [tup[0] for tup in db_management.select_all('CurrentRides', ['WorkerID'])]
    if worker_id in riding_workers:
        return worker_gets_out(worker_id)
    else:
        return worker_gets_in(worker_id, bus_id)


def worker_gets_in(worker_id: int, bus_id: int):
    try:
        max_ride_id = max([tup[0] for tup in db_management.select_all('CurrentRides', ['RideID'])])
    except ValueError:
        max_ride_id = 0
    db_management.insert('CurrentRides', (max_ride_id + 1, worker_id, bus_id, 0))
    return f'Worker {worker_id} gets into the bus {bus_id}'


def worker_gets_out(worker_id: int):
    db_management.delete('CurrentRides', ('WorkerID', worker_id))
    current_balance = db_management.select('Workers', ['WorkerBalance'], [('WorkerID', worker_id)])[0][0]
    db_management.update('Workers', ('WorkerBalance', current_balance - 1.0), ('WorkerID', worker_id))
    return f'Worker {worker_id} gets out from the bus'


if __name__ == "__main__":
    run_mqtt_server()
