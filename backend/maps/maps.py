import googlemaps
import os
import json

class GoogleMapsQuery():
    def __init__(self, api_key) -> None:
        self.g_client: googlemaps.Client = googlemaps.Client(key=api_key)

    def query_pubs(self, long_lat: tuple[float, float], radius):
        query = self.g_client.places_nearby(location={'lat': long_lat[0], 'lng': long_lat[1]},
                                            radius=radius, type='bar')

        print(json.dumps(query))

if __name__ == "__main__":
    key = os.environ.get('KEY')
    g_maps = GoogleMapsQuery(key)
    g_maps.query_pubs((56.3398, -2.7967), 2000)