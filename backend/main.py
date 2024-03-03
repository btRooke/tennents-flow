from simsocket import server
import asyncio

if __name__ == "__main__":
    s = server.SimSocket(8001)
    asyncio.run(s.run())