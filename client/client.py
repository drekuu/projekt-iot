#!/usr/bin/env python3

from http import server
from config import *
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from mfrc522 import MFRC522
import threading
import time
import sys
import datetime
from models import *
from ui import *

rfid = MFRC522()
server_ip = "10.108.33.124"

route_index = 0
routes: list[Route] = []
current_stop_index: int = None
client = mqtt.Client()
stop_rfid_polling = False
last_card_scan_value_time: (int, datetime.datetime) = (None, None)


def on_encoder_left_while_selecting_route() -> None:
    global route_index
    global routes
    if route_index > 0:
        route_index -= 1
        draw_routes_menu(routes, route_index)

def on_encoder_right_while_selecting_route() -> None:
    global route_index
    global routes
    if route_index < len(routes) - 1:
        route_index += 1
        draw_routes_menu(routes, route_index)

def on_green_button_while_on_route() -> None:
    global current_stop_index
    global routes
    global route_index
    route = routes[route_index]
    if current_stop_index < len(route.stops) - 1:
        current_stop_index += 1
        draw_stops_screen(route, current_stop_index)
        client.publish("worker/notify", f"NEXT;{routes[route_index].name};{current_stop_index}")
    else:
        GPIO.remove_event_detect(greenButton)
        GPIO.remove_event_detect(redButton)
        client.publish("worker/notify", f"FINISH;{routes[route_index].name}")
        route_index = 0
        select_route()

def on_red_button_while_on_route() -> None:
    global current_stop_index
    global route_index
    global stop_rfid_polling
    GPIO.remove_event_detect(greenButton)
    GPIO.remove_event_detect(redButton)
    route_index = 0
    stop_rfid_polling = True
    current_stop_index = None
    client.publish("worker/notify", f"END;{routes[route_index].name}")
    select_route()

def on_green_pressed_while_selecting_route() -> None:
    GPIO.remove_event_detect(encoderLeft)
    GPIO.remove_event_detect(encoderRight)
    GPIO.remove_event_detect(greenButton)
    begin_route()

def on_card_scanned(uid: int) -> None:
    global last_card_scan_value_time
    global current_stop_index
    global routes
    global route_index
    (last_value, last_time) = last_card_scan_value_time
    if last_time is not None and last_time + datetime.timedelta(seconds=7) < datetime.datetime.now():
        return
    last_card_scan_value_time = (uid, datetime.datetime.now())
    client.publish("worker/notify", f"{uid};{routes[route_index].name};{current_stop_index}")

def listen_rfid() -> None:
    global stop_rfid_polling
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
        time.sleep(0.5)
    sys.exit()

def select_route() -> Route:
    global routes
    global route_index
    GPIO.add_event_detect(encoderLeft, GPIO.FALLING, callback=on_encoder_left_while_selecting_route, bouncetime=100)
    GPIO.add_event_detect(encoderRight, GPIO.FALLING, callback=on_encoder_right_while_selecting_route, bouncetime=100)
    GPIO.add_event_detect(greenButton, GPIO.FALLING, callback=on_green_pressed_while_selecting_route, bouncetime=100)
    draw_routes_menu(routes, route_index)


def begin_route() -> None:
    global stop_rfid_polling
    global current_stop_index
    global routes
    global route_index
    current_stop_index = 0
    GPIO.add_event_detect(greenButton, GPIO.FALLING, callback=on_green_button_while_on_route, bouncetime=100)
    GPIO.add_event_detect(redButton, GPIO.FALLING, callback=on_red_button_while_on_route, bouncetime=100)
    client.publish("worker/notify", f"START;{routes[route_index].name}")
    draw_stops_screen(routes[route_index], current_stop_index)
    stop_rfid_polling = False
    rfid_thread = threading.Thread(target=listen_rfid)
    rfid_thread.daemon = True
    rfid_thread.start()


def on_mqtt_message(client, userdata, message):
    message_decoded = str(message.payload.decode('utf-8'))
    print(f'Message received: {message_decoded}')
    draw_message(message_decoded)
    timer = threading.Timer(7, draw_stops_screen, args=(routes[route_index], current_stop_index))
    timer.start()

if __name__ == "__main__":
    disp.Init()
    disp.clear()

    client.connect("localhost")
    client.on_message = on_mqtt_message
    client.loop_start()
    client.subscribe("server/notify")

    r1s1 = Stop("Os. Sobieskiego")
    r1s2 = Stop("Szymanowskiego")
    r1s3 = Stop("Kurpinskiego")
    r1s4 = Stop("Al. Solidarnosci")
    route1 = Route("Tramwaj 16", [r1s1, r1s2, r1s3, r1s4])
    route2 = Route("Tramwaj 12", [])
    route3 = Route("Tramwaj 14", [])
    route4 = Route("Autobus 169", [])
    routes = [route1, route2, route3, route4]
    select_route()
