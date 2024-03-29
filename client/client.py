#!/usr/bin/env python3

from typing import Tuple
from config import *
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from mfrc522 import MFRC522
import threading
import time
import datetime
from models import *
from ui import *
import urllib.request, json

rfid = MFRC522()
server_ip = "10.108.33.123"

bus_id = 0

route_index = 0
routes: list[Route] = []
current_stop_index: int = None
client = mqtt.Client()
stop_rfid_polling = False
last_card_scan_value_time: Tuple[int, datetime.datetime] = (None, None)
last_encoder_event: datetime.datetime = None


def on_encoder_left_while_selecting_route(_) -> None:
    global route_index
    global routes
    global last_encoder_event
    if last_encoder_event is not None and last_encoder_event + datetime.timedelta(seconds=0.5) > datetime.datetime.now():
        return
    last_encoder_event = datetime.datetime.now()
    if route_index > 0:
        route_index -= 1
        draw_routes_menu(routes, route_index)

def on_encoder_right_while_selecting_route(_) -> None:
    global route_index
    global routes
    global last_encoder_event
    if last_encoder_event is not None and last_encoder_event + datetime.timedelta(seconds=0.5) > datetime.datetime.now():
        return
    last_encoder_event = datetime.datetime.now()
    if route_index < len(routes) - 1:
        route_index += 1
        draw_routes_menu(routes, route_index)

def on_green_button_while_on_route(_) -> None:
    global current_stop_index
    global routes
    global route_index
    global stop_rfid_polling

    route = routes[route_index]
    client.publish("buses/driver", f"next_stop?bus={bus_id}")
    if current_stop_index < len(route.stops) - 1:
        current_stop_index += 1
        draw_stops_screen(route, current_stop_index)
    else:
        stop_rfid_polling = True
        GPIO.remove_event_detect(buttonGreen)
        route_index = 0
        current_stop_index = 0
        select_route()
        

def on_green_pressed_while_selecting_route(_) -> None:
    GPIO.remove_event_detect(encoderLeft)
    GPIO.remove_event_detect(encoderRight)
    GPIO.remove_event_detect(buttonGreen)
    begin_route()

def on_card_scanned(uid: list[int]) -> None:
    global last_card_scan_value_time
    global current_stop_index
    global routes
    global route_index
    uid_int = int(''.join(list(map(lambda e: str(e), uid))))
    print(f'scanned {uid_int}')
    (last_value, last_time) = last_card_scan_value_time
    if last_time is not None and last_time + datetime.timedelta(seconds=7) > datetime.datetime.now():
        return
    last_card_scan_value_time = (uid_int, datetime.datetime.now())
    client.publish("buses/worker", f"use_card?card={uid_int}&bus={bus_id}")

def listen_rfid() -> None:
    global stop_rfid_polling
    MIFAREReader = MFRC522()
    while True:
        if stop_rfid_polling:
            stop_rfid_polling = False
            break
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                on_card_scanned(uid)
        # this sleep is okay, since this function runs on a separate thread
        time.sleep(1)
    #sys.exit()

def select_route() -> Route:
    global routes
    global route_index
    timer = threading.Timer(3, add_route_selection_callbacks)
    timer.start()
    draw_routes_menu(routes, route_index)

def add_route_selection_callbacks():
    GPIO.add_event_detect(encoderLeft, GPIO.FALLING, callback=on_encoder_left_while_selecting_route, bouncetime=500)
    GPIO.add_event_detect(encoderRight, GPIO.FALLING, callback=on_encoder_right_while_selecting_route, bouncetime=500)
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=on_green_pressed_while_selecting_route, bouncetime=500)


def begin_route() -> None:
    global stop_rfid_polling
    global current_stop_index
    global routes
    global route_index
    current_stop_index = 0
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=on_green_button_while_on_route, bouncetime=500)
    client.publish("buses/driver", f"choose_course?bus={bus_id}&course={routes[route_index].name}")
    draw_stops_screen(routes[route_index], current_stop_index)
    stop_rfid_polling = False
    rfid_thread = threading.Thread(target=listen_rfid)
    rfid_thread.daemon = True
    rfid_thread.start()


def handle_buzzer() -> None:
    GPIO.output(buzzer, GPIO.LOW)
    time.sleep(1)
    GPIO.output(buzzer, GPIO.HIGH)


def on_mqtt_message(client, userdata, message):
    message_decoded = str(message.payload.decode('utf-8'))
    print(f'message received: {message_decoded}')
    draw_message(message_decoded)
    timer = threading.Timer(7, draw_stops_screen, args=(routes[route_index], current_stop_index))
    timer.start()
    if "Invalid card" in message_decoded:
        buzzer_thread = threading.Thread(target=handle_buzzer)
        buzzer_thread.daemon = True
        buzzer_thread.start()
    

def fetch_routes() -> list[Route]:
    with urllib.request.urlopen(f'http://{server_ip}:55555/courses') as url:
        data = json.load(url)
        for route_name in data:
            stops = map(lambda stop_name: Stop(stop_name), data[route_name])
            routes.append(Route(route_name, list(stops)))
    return routes


if __name__ == "__main__":
    try:
        disp.Init()
        disp.clear()

        client.connect(server_ip)
        client.on_message = on_mqtt_message
        client.loop_start()
        client.subscribe("response/#")

        routes = fetch_routes()

        # r1s1 = Stop("Os. Sobieskiego")
        # r1s2 = Stop("Szymanowskiego")
        # r1s3 = Stop("Kurpinskiego")
        # r1s4 = Stop("Al. Solidarnosci")
        # route1 = Route("Tramwaj 16", [r1s1, r1s2, r1s3, r1s4])
        # route2 = Route("Tramwaj 12", [r1s1, r1s2, r1s3, r1s4])
        # route3 = Route("Tramwaj 14", [r1s1, r1s2, r1s3, r1s4])
        # route4 = Route("Autobus 169", [r1s1, r1s2, r1s3, r1s4])
        # routes = [route1, route2, route3, route4]
        select_route()

        while True:
            _ = input()
    except Exception as e:
        print('cleaning up')
        GPIO.cleanup()
        raise e
    except KeyboardInterrupt as e:
        print('cleaning up')
        GPIO.cleanup()
        raise e
