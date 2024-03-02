import asyncio
import websockets
import json

async def handler(websocket):
    async for message in websocket:
        event = json.loads(message)
        print(event["type"])

        response_event = {
            "type": "hello",
        }

        await websocket.send(json.dumps(response_event))

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())