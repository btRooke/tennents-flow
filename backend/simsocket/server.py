import asyncio
from typing import Any
import websockets
import json
from maps import maps
from frontend import conv

INIT_EVENT = "init"

class SimSocket():
    map_query: maps.GoogleMapsQuery
    port: int
    def __init__(self, port: int) -> None:
        self.port = port
        self.map_query = maps.GoogleMapsQuery()

    def generate_world(self):
        return self.map_query.query_pubs((56.3398, -2.7967), 2000)

    async def handle_init(self, websocket: Any):
        pubs = self.generate_world()
        frontend_pubs = conv.convert_pubs(pubs)

        response = {
            "type": "init",
            "pubs": list(map(lambda pub: pub.__dict__, frontend_pubs)),
        }

        print(response)

        await websocket.send(json.dumps(response))

    async def _handler(self, websocket: Any):
        async for message in websocket:
            event = json.loads(message)
            event_type = event["type"]

            if event_type == INIT_EVENT:
                await self.handle_init(websocket)

    async def run(self):
        async with websockets.serve(self._handler, "", self.port):
            await asyncio.Future()


async def handler(websocket):
    async for message in websocket:
        event = json.loads(message)
        print(event["type"])

        response_event = {
            "type": "hello",
        }

        await websocket.send(json.dumps(response_event))