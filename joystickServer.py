import asyncio
import websockets

async def incoming_handler(websocket, path):
    name = await websocket.recv()
    print(name)
    await websocket.send("ok")

start_server = websockets.serve(incoming_handler, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
