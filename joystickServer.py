import asyncio
import websockets
import serial
import RPi.GPIO as gp

# Setup GPIO pins
gp.setmode(gp.BOARD)
gp.setup(16, gp.OUT)
gp.setup(18, gp.OUT)
gp.output(16,1)
gp.output(18,1)

limit=2000
steering_damping = 4
rly1_state=0
rly2_state=1

try:
  s = serial.Serial('/dev/ttyS0',9600)
except:
  print("Unable to open serial connection")
  s=0
  pass

def constrain(x):
  if x > 1:
    return int(1.0)
  elif x < -1:
    return int(-1.0)
  else:
    return x

def relay(pin):
  global rly1_state, rly2_state
  if pin == 0:
    rly1_state = not rly1_state
    gp.output(16, rly1_state)
  elif pin == 1:
    rly2_state = not rly2_state
    gp.output(18, rly2_state)

def go(d,t):
  d=int(d)
  t=int(t)
  address=128
  if d >= 0:
    motor1=chr(address)+chr(0)+chr(d)+chr((address+0+d)&127)
  else:
    d=abs(d)
    motor1=chr(address)+chr(1)+chr(d)+chr((address+1+d)&127)
  if t >= 0:
    motor2=chr(address)+chr(4)+chr(t)+chr((address+4+t)&127)
  else:
    t=abs(t)
    motor2=chr(address)+chr(5)+chr(t)+chr((address+5+t)&127)
  if(s!=0):
    s.write(motor1.encode("UTF-8"))
    s.write(motor2.encode("UTF-8"))

def scale(x, y):
  global limit
  x=constrain(x)
  y=constrain(y)
  l=(y**3)*254*-1
  r=x*254
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
  if dataRecvd[0].__contains__('button'):
    button=int(dataRecvd[1])
    relay(button)

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

