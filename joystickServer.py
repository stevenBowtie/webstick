import asyncio
import websockets

async def incoming_handler(websocket, path):
    while websocket.open:
      name = await websocket.recv()
      print(name)
      websocket.pong()
    websocket.close()

start_server = websockets.serve(incoming_handler, '0.0.0.0', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
