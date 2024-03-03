import googlemaps
from maps import map_types
import os

class GoogleMapsQuery():
    def __init__(self) -> None:
        api_key: str = os.environ['KEY']
        self.g_client: googlemaps.Client = googlemaps.Client(key=api_key)

    def _construct_pub(self, g_bar) -> map_types.Pub:
        the_pub = map_types.Pub()

        long_lat_dict = the_pub['geometry']['location']
        the_pub.coordinates = [long_lat_dict['lat'], long_lat_dict['lang']]
        the_pub.name = the_pub['name']
        the_pub.average_stay = 0
        the_pub.average_wait = 0
        the_pub.capacity = 0
        the_pub.drink_cost = 5
        the_pub.closing_time = ""
        return the_pub


    def query_pubs(self, long_lat: tuple[float, float], radius: int) -> list[map_types.Pub]:
        query = self.g_client.places_nearby(location={'lat': long_lat[0], 'lng': long_lat[1]},
                                            radius=radius, type='bar')

        pubs: list[map_types.Pub] = []

        for result in query['results']:
            pub = self._construct_pub(result)
            pubs.append(pub)

        return pubs