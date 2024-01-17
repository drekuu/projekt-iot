import json

class Stop:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def from_json(text: str):
        parsed = json.loads(text)
        return Stop(parsed['name'])


class Route:
    def __init__(self, name: str, stops: list[Stop]):
        self.name = name
        self.stops = stops

    @staticmethod
    def from_json(text: str):
        parsed = json.loads(text)
        stops = []
        for stop in parsed['stops']:
            stops.append(Stop.from_json(json.dumps(stop)))
        return Route(parsed['name'], stops)
