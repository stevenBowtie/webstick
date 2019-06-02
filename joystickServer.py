import asyncio
import websockets
import serial

limit=2000
steering_damping = 4

try:
  s = serial.Serial('/dev/ttyACM0',115200)
except:
  print("Unable to open serial connection")
  s=0
  pass

def go(d,t):
  goStr="M1: {} \r\nM2: {} \r\n".format(d,t)
  print(goStr)
  if(s!=0):
    s.write(goStr.encode("UTF-8"))

def scale(x, y):
  global limit
  l=int((y*limit)+(-x*(limit/steering_damping)))
  r=int((y*limit)+(x*(limit/steering_damping)))
  go(l,r)

def parse(dataRecvd):
  global limit
  dataRecvd=dataRecvd.split(',')
  if dataRecvd[0].__contains__('drive'):
    x = float( dataRecvd[1] )
    y = float( dataRecvd[2] )
    scale(x, y)
  if dataRecvd[0].__contains__('limit'):
    limit=int(dataRecvd[1])
    print(limit)

async def incoming_handler(websocket, path):
  while websocket.open:
    name = await websocket.recv()
    print(name)
    parse(name)
    websocket.pong()
  websocket.close()

start_server = websockets.serve(incoming_handler, '0.0.0.0', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

