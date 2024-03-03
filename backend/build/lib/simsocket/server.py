import asyncio
from typing import Any
import websockets
import json
from maps import maps
from maps import map_types
from frontend import conv
from frontend import frontend_mock

INIT_EVENT = "init"
NEXT_STEP = "next_step"

class SimSocket():
    map_query: maps.GoogleMapsQuery
    port: int
    pubs: list[map_types.Pub]
    def __init__(self, port: int) -> None:
        self.port = port
        self.map_query = maps.GoogleMapsQuery()
        self.pubs = []

    def generate_world(self):
        return self.map_query.query_pubs((56.3398, -2.7967), 2000)

    async def handle_init(self, websocket: Any):
        pubs = self.generate_world()
        frontend_pubs = conv.convert_pubs(pubs)
        self.pubs = pubs

        response = {
            "type": INIT_EVENT,
            "pubs": list(map(lambda pub: pub.__dict__, frontend_pubs)),
        }

        await websocket.send(json.dumps(response))

    async def handle_next_step(self, websocket: Any):
        pubs = list(map(lambda p: p.name, self.pubs))

        next_step_event = {
            "type": NEXT_STEP,
            "data": {
                "agents": frontend_mock.generate_random_actors(1000, pubs),
                "revenue": frontend_mock.generate_random_business(pubs),
            }
        }

        await websocket.send(json.dumps(next_step_event))

    async def _handler(self, websocket: Any):
        async for message in websocket:
            event = json.loads(message)
            event_type = event["type"]

            if event_type == INIT_EVENT:
                await self.handle_init(websocket)
            if event_type == NEXT_STEP:
                await self.handle_next_step(websocket)

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