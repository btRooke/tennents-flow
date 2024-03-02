from maps import map_types
from frontend import frontend_types

MAP_SIZE = 10

def normalise_coordinates(coords: tuple[float, float]) -> tuple[float, float]:
    return coords[0], coords[1]

def convert_to_frontend(backend_pub: map_types.Pub) -> frontend_types.Pub:
    pub = frontend_types.Pub()
    pub.coordinates = backend_pub.coordinates
    pub.name = backend_pub.name
    return pub

def convert_pubs(pubs: list[map_types.Pub]) -> list[frontend_types.Pub]:
    frontend_pubs = list(map(convert_to_frontend, pubs))

    lat_range: tuple[float, float] = (float("inf"), float("-inf"))
    long_range: tuple[float, float] = (float("inf"), float("-inf"))

    for pub in frontend_pubs:
        lat_range = (min(lat_range[0], pub.coordinates[0]), max(lat_range[1], pub.coordinates[0]))
        long_range = (min(long_range[0], pub.coordinates[1]), max(long_range[1], pub.coordinates[1]))

    for pub in frontend_pubs:
        lat, long = pub.coordinates
        x = 2 * MAP_SIZE * ((lat - lat_range[0]) / (lat_range[1] - lat_range[0])) + -MAP_SIZE
        y = 2 * MAP_SIZE * ((long - long_range[0]) / (long_range[1] - long_range[0])) + -MAP_SIZE
        pub.coordinates = (x, y)

    return frontend_pubs