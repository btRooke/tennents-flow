from maps import map_types
from frontend import frontend_types
from pubsim.utils import utils

MAP_SIZE = 10

def normalise_coordinates(coords: tuple[float, float]) -> tuple[float, float]:
    return coords[0], coords[1]

def convert_to_frontend(backend_pub: map_types.Pub) -> frontend_types.Pub:
    pub = frontend_types.Pub()
    pub.location = backend_pub.location
    pub.name = backend_pub.name
    pub.size = backend_pub.size
    return pub

def convert_pubs(pubs: list[map_types.Pub]) -> list[frontend_types.Pub]:
    frontend_pubs = list(map(convert_to_frontend, pubs))

    lat_range: tuple[float, float] = (float("inf"), float("-inf"))
    long_range: tuple[float, float] = (float("inf"), float("-inf"))

    for pub in frontend_pubs:
        lat_range = (min(lat_range[0], pub.location[0]), max(lat_range[1], pub.location[0]))
        long_range = (min(long_range[0], pub.location[1]), max(long_range[1], pub.location[1]))

    for pub in frontend_pubs:
        lat, long = pub.location
        x = 2 * MAP_SIZE * ((lat - lat_range[0]) / (lat_range[1] - lat_range[0])) + -MAP_SIZE
        y = 2 * MAP_SIZE * ((long - long_range[0]) / (long_range[1] - long_range[0])) + -MAP_SIZE
        pub.location = (x, y)

    return frontend_pubs
