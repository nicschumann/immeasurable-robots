import signal
import sys

import time
import board
import digitalio
import busio

# signals
def sigint_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

# Pinouts
A0_switch = digitalio.DigitalInOut(board.D4)
B0_switch = digitalio.DigitalInOut(board.D17)
C0_switch = digitalio.DigitalInOut(board.D27)
C1_switch = digitalio.DigitalInOut(board.D14)
B1_switch = digitalio.DigitalInOut(board.D15)
A1_switch = digitalio.DigitalInOut(board.D18)

# Enable Pulldown Resistors
A0_switch.pull = digitalio.Pull.DOWN
B0_switch.pull = digitalio.Pull.DOWN
C0_switch.pull = digitalio.Pull.DOWN
C1_switch.pull = digitalio.Pull.DOWN
B1_switch.pull = digitalio.Pull.DOWN
A1_switch.pull = digitalio.Pull.DOWN


# Switch definitions
pin_names = ["A0 switch", "B0 switch", "C0 switch", "C1 switch", "B1 switch", "A1 switch"]
pins = [A0_switch, B0_switch, C0_switch, C1_switch, B1_switch, A1_switch]
seen = [False] * len(pins)

while True:
    triggered = [*map(lambda i: pins[i].value and not seen[i], range(len(pins)))]

    for i in range(len(triggered)):
        if triggered[i]:
            print('%s triggered' % pin_names[i])
            seen[i] = True

        if not pins[i].value:
            seen[i] = False

    time.sleep(0.01)
