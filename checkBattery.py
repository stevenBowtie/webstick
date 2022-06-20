#!/usr/bin/python
import serial
from time import sleep
#ser=serial.Serial('/dev/ttyAMA0',38400)
ser=serial.Serial('/dev/ttyACM0',115200)
ser.write( "M1:getb\r\n".encode() )
sleep(.5)
print( ser.read(ser.inWaiting() ) )
#voltage=int(ser.read())/10.0
#print voltage
ser.close()
exit()
