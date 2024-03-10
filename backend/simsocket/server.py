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
import os
import ssl

if "SSL_CERT" in os.environ:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_cert = os.environ["SSL_CERT"]
    ssl_key = os.environ["SSL_KEY"]
    ssl_context.load_cert_chain(ssl_cert, keyfile=ssl_key)

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

    def _get_data_source(self) -> tuple[str, str]:
        source = ""

        if 'SOURCE' in os.environ:
            source = os.environ['SOURCE']

        if source == 'SPOONS':
            return "./pubsim/spoons_example/StA_spoons_venue_data.json", "./pubsim/spoons_example/StA_spoons_venue_distribution.json"

        return ("./pubsim/example/StA_venue_data.json", "./pubsim/example/StA_venue_distribution.json")

    def generate_world(self):
        return maps.convert_pubsim(self._get_data_source()[0])

    async def handle_init(self, websocket: Any):
        pubs = self.generate_world()
        frontend_pubs = conv.convert_pubs(pubs)
        self.pubs = pubs

        session_id = str(uuid4())

        venue_data, distribution = self._get_data_source()

        print(venue_data, distribution)

        self.uuids[session_id] = PubMap(num_agents=1000, venue_path=venue_data,
                    venue_distribution_path=distribution,
                    seed=144)

        response = {
            "type": INIT_EVENT,
            "pubs": list(map(lambda pub: pub.__dict__, frontend_pubs)),
            "uuid": str(session_id)
        }

        await websocket.send(json.dumps(response))

    async def handle_next_step(self, websocket: Any, event: Any):
        uid = event["uuid"]
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

        if "SSL_CERT" in os.environ:
            async with websockets.serve(self._handler, "", self.port, ssl=ssl_context):
                await asyncio.Future()
        else:
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