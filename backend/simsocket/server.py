import asyncio
from typing import Any
import websockets
import json
from maps import maps
from maps import map_types
from frontend import conv
from frontend import pub_sim
from pubsim.PubMap import PubMap
from uuid import uuid4

INIT_EVENT = "init"
NEXT_STEP = "next_step"

class SimSocket():
    map_query: maps.GoogleMapsQuery
    port: int
    pubs: list[map_types.Pub]
    # maps user UUIDS to their corresponding pubmap session
    uuids: dict[str, PubMap]
    def __init__(self, port: int) -> None:
        self.port = port
        self.map_query = maps.GoogleMapsQuery()
        self.pubs = []
        self.uuids = {}

    def generate_world(self):
        pubs = maps.convert_pubsim('./pubsim/example/StA_spoons_venue_data.json')
        return pubs

    async def handle_init(self, websocket: Any):
        pubs = self.generate_world()
        frontend_pubs = conv.convert_pubs(pubs)
        self.pubs = pubs

        session_id = str(uuid4())

        self.uuids[session_id] = PubMap(num_agents=1000, venue_path="./pubsim/example/StA_spoons_venue_data.json",
                    venue_distribution_path="./pubsim/example/StA_spoons_venue_distribution.json",
                    seed=144)

        response = {
            "type": INIT_EVENT,
            "pubs": list(map(lambda pub: pub.__dict__, frontend_pubs)),
            "uuid": str(session_id)
        }

        await websocket.send(json.dumps(response))

    async def handle_next_step(self, websocket: Any, event: Any):
        uid = event["uuid"]
        print(self.uuids)
        pub_map = self.uuids[uid]
        transitions, revenues = pub_map.step()

        next_step_event = {
            "type": NEXT_STEP,
            "data": {
                "agents": pub_sim.pubsim_transition_to_frontend(transitions),
                "revenue": pub_sim.pubsim_revenue_to_frontend(revenues),
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
                await self.handle_next_step(websocket, event)

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