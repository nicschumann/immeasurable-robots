import time
import board
import digitalio
import busio

pin = digitalio.DigitalInOut(board.D21)

while True:
    if not pin.value:
        print('triggered')
