import numpy as np
import time
import signal
import sys

from joystick import Joystick
from tools import speeds2motors, angError, actuate
from client.serialRadio import SerialRadio

js = Joystick()
serial = SerialRadio()

direction = 1
lastRefAngle = 0

def signal_handler(signal, frame):
    js.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def control(curAngle, refAngle, refVel, curVel, curW, turbo, spin, curBallVel):
    global lastRefAngle
    
    if turbo:
        w = 8 * angError(refAngle, curAngle)
        v = min(2, 7 / np.abs(curW))
    elif spin != 0:
        w = 60 * np.sign(spin)
        v = 0
    else:
        w = 9 * angError(refAngle, curAngle) + 0.01 * (refAngle - lastRefAngle) / 0.016
        v = refVel * 1#min(refVel * 1, 0.4 + (1 - 0.4) * np.exp(-1 * (curW+w)) )

    lastRefAngle = refAngle
    
    return speeds2motors(v * direction, w)

def optimalAngle(angle, direction):
    return angle + (np.pi if direction == -1 else 0)
    
t0 = 0
visionData = None

while True:
    t0 = time.time()
    refAngle = js.angle
    speed = js.speed
    # if speed != 0: print(speed)
    w = js.w
    turbo = js.turbo
    spin = js.spin

    output = []
    
    output.append((speed*3, w))
    output.append((speed*3, w))
    output.append((speed*3, w))
    # if output != [(0,0),(0,0),(0,0)]: print(output)
    
    serial.send(output)
    print(1/(time.time()-t0), flush=True, end="\r")
    # serial.send([(0,0),(0,0),(0,0)])


    #### serial recebe range/tuple de robos que a informação vai ser distribuida  
    #self.radio.send([(0,0) for robot in self.world.team])


js.stop()
