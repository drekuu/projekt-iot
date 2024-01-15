import lib.oled.SSD1331 as SSD1331
from PIL import ImageFont, ImageDraw, Image

from models import *

disp = SSD1331.SSD1331()
fontLarge = ImageFont.truetype('lib/oled/Font.ttf', 15)
fontSmall = ImageFont.truetype('lib/oled/Font.ttf', 13)

def get_blank_image() -> Image:
    return Image.new('RGB', (disp.width, disp.height), 'WHITE')

def draw_routes_menu(routes: list[Route], route_index: int) -> None:
    image = get_blank_image()
    draw = ImageDraw.Draw(image)
    draw.text((8, 0), 'Trasy', font=fontLarge, fill='BLACK')
    if len(routes) == 0:
        draw.text((32, 24), 'BRAK', font=fontLarge, fill='BLACK')
    else:
        routes_to_display = [None, None, None]
        selected_on_display = 0
        if route_index == 0:
            routes_to_display[0] = routes[0]
            if len(routes) >= 2:
                routes_to_display[1] = routes[1]
                if len(routes) >= 3:
                    routes_to_display[2] = routes[2]
        elif route_index == len(routes) - 1:
            selected_on_display = 2
            routes_to_display[2] = routes[route_index]
            if route_index - 1 >= 0:
                routes_to_display[1] = routes[route_index - 1]
                if route_index - 2 >= 0:
                    routes_to_display[0] = routes[route_index - 2]
        else:
            selected_on_display = 1
            routes_to_display[0] = routes[route_index - 1]
            routes_to_display[1] = routes[route_index]
            routes_to_display[2] = routes[route_index + 1]
        draw.text((16, 20), routes_to_display[0].name, font=fontSmall, fill='BLACK')
        draw.text((16, 32), routes_to_display[1].name, font=fontSmall, fill='BLACK')
        draw.text((16, 44), routes_to_display[2].name, font=fontSmall, fill='BLACK')
        arrow_y_offset = 0
        if selected_on_display == 0:
            arrow_y_offset = 20
        elif selected_on_display == 1:
            arrow_y_offset = 32
        else:
            arrow_y_offset = 44
        draw.text((8, arrow_y_offset), '>', font=fontSmall, fill='BLACK')
    disp.ShowImage(image, 0, 0)


def draw_stops_screen(route: Route, stop_index: int) -> None:
    image = get_blank_image()
    draw = ImageDraw.Draw(image)
    draw.text((8, 0), f'Trasa: {route.name}', font=fontSmall, fill='BLACK')
    draw.text((8, 20), f'Przystanek: {route[stop_index].name}', font=fontLarge, fill='BLACK')
    draw.text((8, 40), f'{stop_index}/{len(route.stops)}', font=fontLarge, fill='BLACK')
    disp.ShowImage(image, 0, 0)


def draw_message(message: str) -> None:
    image = get_blank_image()
    draw = ImageDraw.Draw(image)
    draw.text((8, 0), message, font=fontLarge, fill='BLACK')
    disp.ShowImage(image, 0, 0)