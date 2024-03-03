"""
Pub represents the data type for the pub object between the backend
and the frontend passed by websockets
"""
class Pub():
    coordinates: tuple[float, float]
    name: str