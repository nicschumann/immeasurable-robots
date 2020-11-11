import signal
import sys

import time
import board
import digitalio
import busio

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

# signals
def sigint_handler(sig, frame):
    for M in rails: M.release()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)


# ConvenienceConstants
FORWARD = stepper.FORWARD
BACKWARD = stepper.BACKWARD

# Boards and Interfaces

K0 = MotorKit(address=0x60)
K1 = MotorKit(address=0x61)

M1 = K0.stepper1
M2 = K1.stepper1

P1 = digitalio.DigitalInOut(board.D20)
P2 = digitalio.DigitalInOut(board.D21)

P1.pull = digitalio.Pull.DOWN
P2.pull = digitalio.Pull.DOWN

# Data Arrays
rails       = [M1, M2]
pins        = [P1, P2]
seen        = [False, False]
directions  = [FORWARD, FORWARD]


while True:
    triggered = [*map(lambda i: pins[i].value and not seen[i], range(len(rails)))]

    for i in range(len(rails)):
        if triggered[i]:
            print("switch %i was triggered" % i)
            directions[i] = BACKWARD if directions[i] == FORWARD else FORWARD
            seen[i] = True

        if not pins[i].value:
            seen[i] = False

    for i in range(len(rails)):
        rails[i].onestep(
            direction=directions[i],
            style=stepper.INTERLEAVE)

    time.sleep(0.01)
