import asyncio
import time
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

def parse( ws_string, ws_handle ):
  global limit
  v_str=''
  dataRecvd=ws_string.split(',')
  if dataRecvd[0].__contains__('drive'):
    x = float( dataRecvd[1] )
    y = float( dataRecvd[2] )
    scale(x, y)
  if dataRecvd[0].__contains__('limit'):
    limit=int(dataRecvd[1])
    print(limit)
  if dataRecvd[0].__contains__('battery'):
    s.write( "M1:getb\r\n".encode() )
    loop_limit=0
    while s.inWaiting() < 9:
      loop_limit+=1
      if loop_limit > 1000000:
        break
    v_str = str( s.read( s.inWaiting() ).decode() )
    v_str = v_str.split("M1:B")
    v_str = v_str[1].split("\r\n")
    v_str = str( int(v_str[0])/10.0 )
  return v_str

async def incoming_handler(websocket, path):
  while websocket.open:
    name = await websocket.recv()
    derp = parse( name, websocket )
    await websocket.send( derp )
    websocket.pong()
  websocket.close()

start_server = websockets.serve(incoming_handler, '0.0.0.0', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

