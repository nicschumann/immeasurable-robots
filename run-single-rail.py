import signal
import sys
import argparse

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

# pick the rail to control based on a command line flag
parser = argparse.ArgumentParser(description="Run single rail program.")
parser.add_argument('--rail', dest="rail", type=str, help="Specify the rail this script should control.")
args = parser.parse_args()


if args.rail == 'A0':
    motorkit_address = 0x60
    switch_address = board.D4
    kit = MotorKit(address=motorkit_address)
    motor = kit.stepper1

elif args.rail == 'B0':
    motorkit_address = 0x60
    switch_address = board.D17
    kit = MotorKit(address=motorkit_address)
    motor = kit.stepper2

elif args.rail == 'C0':
    motorkit_address = 0x61
    switch_address = board.D27
    kit = MotorKit(address=motorkit_address)
    motor = kit.stepper1

elif args.rail == 'C1':
    motorkit_address = 0x61
    switch_address = board.D14
    kit = MotorKit(address=motorkit_address)
    motor = kit.stepper2

elif args.rail == 'B1':
    motorkit_address = 0x62
    switch_address = board.D15
    kit = MotorKit(address=motorkit_address)
    motor = kit.stepper1

elif args.rail == 'A1':
    motorkit_address = 0x62
    switch_address = board.D18
    kit = MotorKit(address=motorkit_address)
    motor = kit.stepper2

else:
    print("Please specify the target rail as one of A0, B0, C0, C1, B1, A1.")
    exit(1)

# Boards and Interfaces / Switches

switch = digitalio.DigitalInOut(switch_address)
switch.pull = digitalio.Pull.DOWN

# Data and State Arrays

rails       = [motor]
pins        = [switch]
seen        = [False]
directions  = [FORWARD]
steps       = [0]
limits      = [400]

# Rail logic

while True:
    triggered = [*map(lambda i: pins[i].value and not seen[i], range(len(rails)))]

    for i in range(len(rails)):
        if triggered[i]:
            # print("switch was triggered")
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

    time.sleep(0.01)
