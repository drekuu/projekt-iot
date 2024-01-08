#!/usr/bin/env python3

import lib.oled.SSD1331 as SSD1331
from PIL import ImageFont, ImageDraw, Image
from config import *
import RPi.GPIO as GPIO

disp = SSD1331.SSD1331()
fontLarge = ImageFont.truetype('lib/oled/Font.ttf', 15)
fontSmall = ImageFont.truetype('lib/oled/Font.ttf', 13)


class Stop:
    def __init__(self, name: str):
        self.name = name


class Route:
    def __init__(self, name: str, stops: list[str]):
        self.name = name
        self.stops = stops


def get_blank_image() -> Image:
    return Image.new("RGB", (disp.width, disp.height), "WHITE")


def draw_route_menu(routes: list[Route], selected: int) -> None:
    image = get_blank_image()
    draw = ImageDraw.Draw(image)
    draw.text((8, 0), u'Trasy', font=fontLarge, fill="BLACK")
    if (len(routes) == 0):
        draw.text((32, 24), u'BRAK', font=fontLarge, fill="BLACK")
    else:
        routes_to_display = [None, None, None]
        selected_on_display = 0
        if selected == 0:
            routes_to_display[0] = routes[0]
            if len(routes) >= 2:
                routes_to_display[1] = routes[1]
                if len(routes) >= 3:
                    routes_to_display[2] = routes[2]
        elif selected == len(routes) - 1:
            selected_on_display = 2
            routes_to_display[2] = routes[selected]
            if selected - 1 >= 0:
                routes_to_display[1] = routes[selected - 1]
                if selected - 2 >= 0:
                    routes_to_display[0] = routes[selected - 2]
        else:
            selected_on_display = 1
            routes_to_display[0] = routes[selected - 1]
            routes_to_display[1] = routes[selected]
            routes_to_display[2] = routes[selected + 1]
        draw.text((16, 20), routes_to_display[0].name, font=fontSmall, fill="BLACK")
        draw.text((16, 32), routes_to_display[1].name, font=fontSmall, fill="BLACK")
        draw.text((16, 44), routes_to_display[2].name, font=fontSmall, fill="BLACK")
        arrow_y_offset = 0
        if selected_on_display == 0:
            arrow_y_offset = 20
        elif selected_on_display == 1:
            arrow_y_offset = 32
        else:
            arrow_y_offset = 44
        draw.text((8, arrow_y_offset), '>', font=fontSmall, fill="BLACK")


    disp.ShowImage(image, 0, 0)


def select_route(routes: list[Route]) -> Route:
    route_index = 0
    GPIO.add_event_detect(encoderLeft, GPIO.FALLING, callback=buttonPressedCallback, bouncetime=200)
    GPIO.add_event_detect(encoderRight, GPIO.FALLING, callback=buttonPressedCallback, bouncetime=200)
    draw_route_menu(routes, 0)
    while True:
        pass


if __name__ == "__main__":
    disp.Init()
    disp.clear()
    r1s1 = Stop("Os. Sobieskiego")
    r1s2 = Stop("Szymanowskiego")
    r1s3 = Stop("Kurpinskiego")
    r1s4 = Stop("Al. Solidarnosci")
    route1 = Route("Tramwaj 16", [r1s1, r1s2, r1s3, r1s4])
    route2 = Route("Tramwaj 12", [])
    route3 = Route("Tramwaj 14", [])
    route4 = Route("Autobus 169", [])
    select_route([route1, route2, route3, route4])
