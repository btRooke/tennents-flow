import googlemaps
from maps import map_types

class GoogleMapsQuery():
    def __init__(self, api_key) -> None:
        self.g_client: googlemaps.Client = googlemaps.Client(key=api_key)

    def query_pubs(self, long_lat: tuple[float, float], radius: int) -> list[map_types.Pub]:
        query = self.g_client.places_nearby(location={'lat': long_lat[0], 'lng': long_lat[1]},
                                            radius=radius, type='bar')


        print(query)

        return []