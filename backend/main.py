import os
from maps import maps

if __name__ == "__main__":
    key = os.environ.get('KEY')
    g_maps = maps.GoogleMapsQuery(key)
    g_maps.query_pubs((56.3398, -2.7967), 2000)