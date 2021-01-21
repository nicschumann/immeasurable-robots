import signal
import sys
import argparse

import time
import board
import digitalio
import busio

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

import pdb

# signals
def sigint_handler(sig, frame):
    for M in rails: M.release()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

# Convenience Constants

FORWARD = stepper.FORWARD
BACKWARD = stepper.BACKWARD

# enum specifying the states
# of the switch configuration
SWITCH_IDLE = 0
SWITCH_TRIGGERED = 1
SWITCH_HANDLED = 2

# pick the rail to control based on a command line flag
parser = argparse.ArgumentParser(description="Run single rail program.")
parser.add_argument('--rail', dest="rail", type=str, help="Specify the rail this script should control.")
args = parser.parse_args()


if args.rail == 'A0':
    motorkit_address = 0x60
    switch_address = board.D4
    kit = MotorKit(address=motorkit_address)
    motor = kit.stepper1
    limit = 2588

elif args.rail == 'B0':
    motorkit_address = 0x60
    switch_address = board.D17
    kit = MotorKit(address=motorkit_address)
    motor = kit.stepper2
    limit = 4500

elif args.rail == 'C0':
    motorkit_address = 0x61
    switch_address = board.D27
    kit = MotorKit(address=motorkit_address)
    motor = kit.stepper1
    limit = 5574

elif args.rail == 'C1':
    motorkit_address = 0x61
    switch_address = board.D14
    kit = MotorKit(address=motorkit_address)
    motor = kit.stepper2
    limit = 5615

elif args.rail == 'B1':
    motorkit_address = 0x62
    switch_address = board.D15
    kit = MotorKit(address=motorkit_address)
    motor = kit.stepper1
    limit = 4755

elif args.rail == 'A1':
    motorkit_address = 0x62
    switch_address = board.D18
    kit = MotorKit(address=motorkit_address)
    motor = kit.stepper2
    limit = 2600

else:
    print("Please specify the target rail as one of A0, B0, C0, C1, B1, A1.")
    exit(1)

# Boards and Interfaces / Switches

switch = digitalio.DigitalInOut(switch_address)
switch.pull = digitalio.Pull.DOWN

# Data and State Arrays

rails       = [motor]
pins        = [switch]
seen        = [SWITCH_IDLE]
directions  = [FORWARD]
steps       = [0]
limits      = [limit]

# Rail logic

while True:
    triggered = switch.value and seen[0] == SWITCH_IDLE

    if triggered:
        # breakpoint()
        directions[0] = BACKWARD if directions[0] == FORWARD else FORWARD
        seen[0] = SWITCH_HANDLED
        steps[0] = -40 # give a small margin around the switch, to avoid hitting it.

    if not switch.value and seen[0] == SWITCH_HANDLED:
        seen[0] = SWITCH_IDLE

    if steps[0] >= limits[0]:
        directions[0] = BACKWARD if directions[0] == FORWARD else FORWARD
        steps[0] = 0

    motor.onestep(direction=directions[0], style=stepper.SINGLE)
    steps[0] += 1

    time.sleep(0.003)
