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

M1 = K0.stepper1
# M2 = K0.stepper1


# signals
def sigint_handler(sig, frame):
    M1.release()
    # M2.release()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)



# Switch definitions.
limits1 = digitalio.DigitalInOut(board.D20)
limits1.pull = digitalio.Pull.DOWN
seen = False

direction = FORWARD

while True:
    triggered = limits1.value and not seen

    if triggered:
        print('limit switch triggered, switch direction')
        direction = BACKWARD if direction == FORWARD else FORWARD
        seen = True

    if not limits1.value:
        seen = False

    M1.onestep(
        direction=direction,
        style=stepper.DOUBLE)

    time.sleep(0.01)
