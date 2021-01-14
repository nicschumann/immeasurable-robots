import signal
import sys

import time
import board
import digitalio
import busio

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

# Boards and Interfaces / Motors

K0 = MotorKit(address=0x60)
K1 = MotorKit(address=0x61)
K2 = MotorKit(address=0x62)

K0.stepper1.release()
K0.stepper2.release()
K1.stepper1.release()
K1.stepper2.release()
K2.stepper1.release()
K2.stepper2.release()
