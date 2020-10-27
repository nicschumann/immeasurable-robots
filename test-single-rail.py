import signal
import sys

import time
import board
import digitalio
import busio

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper


FORWARD = stepper.FORWARD
BACKWARD = stepper.BACKWARD

# Motor Definitions
K0 = MotorKit(address=0x60)
K1 = MotorKit(address=0x61)

M1 = K1.stepper1
M2 = K0.stepper1


# signals
def sigint_handler(sig, frame):
    M1.release()
    M2.release()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

# Switch definitions.
right = digitalio.DigitalInOut(board.D20)
left = digitalio.DigitalInOut(board.D21)
left_seen, right_seen = False, False

direction = FORWARD

while True:
    left_triggered = (not left.value) and not left_seen
    right_triggered = (not right.value) and not right_seen

    if left_triggered:
        print('left limit switch triggered, switch direction')
        direction = BACKWARD if direction == FORWARD else FORWARD
        left_seen = True

    if left.value:
        left_seen = False

    if right_triggered:
        print('right limit switch triggered, switch direction')
        direction = BACKWARD if direction == FORWARD else FORWARD
        right_seen = True

    if right.value:
        right_seen = False

    M1.onestep(
        direction=direction,
        style=stepper.DOUBLE)

    time.sleep(0.01)
