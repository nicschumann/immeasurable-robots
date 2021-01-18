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


 # Convenience Constants

FORWARD = stepper.FORWARD
BACKWARD = stepper.BACKWARD

# Boards and Interfaces / Motors

K0 = MotorKit(address=0x60)
K1 = MotorKit(address=0x61)
K2 = MotorKit(address=0x62)

A0_motor = K0.stepper1
B0_motor = K0.stepper2
C0_motor = K1.stepper1
C1_motor = K1.stepper2
B1_motor = K2.stepper1
A1_motor = K2.stepper2

# Boards and Interfaces / Switches

A0_switch = digitalio.DigitalInOut(board.D4)
B0_switch = digitalio.DigitalInOut(board.D17)
C0_switch = digitalio.DigitalInOut(board.D27)
C1_switch = digitalio.DigitalInOut(board.D14)
B1_switch = digitalio.DigitalInOut(board.D15)
A1_switch = digitalio.DigitalInOut(board.D18)

A0_switch.pull = digitalio.Pull.DOWN
B0_switch.pull = digitalio.Pull.DOWN
C0_switch.pull = digitalio.Pull.DOWN
C1_switch.pull = digitalio.Pull.DOWN
B1_switch.pull = digitalio.Pull.DOWN
A1_switch.pull = digitalio.Pull.DOWN

# Data and State Arrays

rails       = [A0_motor, B0_motor, C0_motor, C1_motor, B1_motor, A1_motor]
pins        = [A0_switch, B0_switch, C0_switch, C1_switch, B1_switch, A1_switch]
seen        = [False] * len(pins)
directions  = [FORWARD] * len(rails)
steps       = [0] * len(rails)
limits      = [400, 400, 400, 400, 400, 400]


# Rail logic

while True:
    triggered = [*map(lambda i: pins[i].value and not seen[i], range(len(rails)))]

    for i in range(len(rails)):
        if triggered[i]:
            # print("switch %i was triggered" % i)
            directions[i] = BACKWARD if directions[i] == FORWARD else FORWARD
            seen[i] = True
            steps[i] = 0

        if not pins[i].value:
            seen[i] = False

    for i in range(len(rails)):
        rails[i].onestep(
            direction=directions[i],
            style=stepper.SINGLE)
        steps[i] += 1

    for i in range(len(rails)):
        if steps[i] >= limits[i]:
            # print("limit was reached")
            directions[i] = BACKWARD if directions[i] == FORWARD else FORWARD
            steps[i] = 0
