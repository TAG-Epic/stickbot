"""
Created by Epic at 8/24/20
"""
from aiohttp import ClientSession
from io import BytesIO


async def stickify(image_bytes):
    fail_counter = 0
    async with ClientSession() as session:
        while True:
            try:
                r = await session.post("https://stick.vote.rip/stickbug", data={"file": image_bytes})
                if r.status != 200:
                    raise ValueError("Invalid response")
                return BytesIO(await r.read())
            except:
                fail_counter += 1
                if fail_counter > 10:
                    raise TimeoutError("Can't connect to server")

