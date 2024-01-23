class Stop:
    def __init__(self, name: str):
        self.name = name


class Route:
    def __init__(self, name: str, stops: list[Stop]):
        self.name = name
        self.stops = stops
