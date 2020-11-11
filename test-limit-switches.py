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
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

P1 = digitalio.DigitalInOut(board.D20)
P2 = digitalio.DigitalInOut(board.D21)

P1.pull = digitalio.Pull.DOWN
P2.pull = digitalio.Pull.DOWN


# Switch definitions
pins = [P1, P2]
seen = [False, False]

while True:
    triggered = [*map(lambda i: pins[i].value and not seen[i], range(len(pins)))]

    for i in range(len(triggered)):
        if triggered[i]:
            print('pin %s triggered' % i)
            seen[i] = True

        if not pins[i].value:
            seen[i] = False

    time.sleep(0.01)
