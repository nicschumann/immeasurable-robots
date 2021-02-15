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

# SPEED

SPEED = stepper.SINGLE

# Cooling Time

DWELL_TIME_STEPS = 120
RUNNING_TIME_S = 5 * 60
COOLING_TIME_S = 2 * 60
COOLING_LONG_TIME_S = 10 * 60
COOLING_LONG_STEPS = 8
TOTAL_RUNNING_TIME_S = 8.5 * 60 * 60

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
limits      = [2588, 4768, 5574, 5615, 4755, 2600]
dwell       = [0] * len(rails)

T           = 0
t           = 0
c           = 0
r_index     = 0

# Railset logic

railsets = [
    [0, 1, 3],
    [2, 4, 5],
    [0, 5],
    [1, 3],
    [2, 4, 5]
    [1, 2, 3, 4],
    [0, 2, 4, 5]
]

# Rail Action

while True:
    s = time.time()
    railset = railsets[r_index]
    triggered = [*map(lambda i: pins[i].value and not seen[i], railset)]

    for i in railset:
        if dwell[i] > 0:
            dwell[i] -= 1;
            continue

        if triggered[i]:
            directions[i] = BACKWARD if directions[i] == FORWARD else FORWARD
            seen[i] = True
            steps[i] = -20

        if not pins[i].value and seen[i] == True:
            seen[i] = False

        if steps[i] >= limits[i]:
            dwell[i] = DWELL_TIME_STEPS
            directions[i] = BACKWARD if directions[i] == FORWARD else FORWARD
            steps[i] = 0

        rails[i].onestep(
            direction=directions[i],
            style=SPEED)

        if dwell[i] == 0:
            steps[i] += 1

        time.sleep(0.003)

    e = time.time()
    t += (e - s)

    if (t > RUNNING_TIME_S):
        T += t
        c += 1
        t = 0
        r_index = (r_index + 1) % len(railsets)

        if (c % COOLING_LONG_STEPS == 0):
            c = 0
            time.sleep(COOLING_LONG_TIME_S)
        else:
            time.sleep(COOLING_TIME_S)

    if (T > TOTAL_RUNNING_TIME_S):
        exit(0)
