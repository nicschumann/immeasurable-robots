import time
import board
import digitalio
import busio

led = digitalio.DigitalInOut(board.D21)
led = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.1)
