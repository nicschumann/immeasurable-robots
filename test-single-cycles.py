import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

K1 = MotorKit(address=0x60)

M1 = K1.stepper1

print("Testing SINGLE stepping...")
for i in range(200):
    M1.onestep(
        direction=stepper.FORWARD,
        style=stepper.SINGLE)
    time.sleep(0.01)

print("Testing DOUBLE stepping...")
for i in range(200):
    M1.onestep(
        direction=stepper.BACKWARD,
        style=stepper.DOUBLE)
    time.sleep(0.01)

print("Testing INTERLEAVE stepping...")
for i in range(200):
    M1.onestep(
        direction=stepper.FORWARD,
        style=stepper.INTERLEAVE)
    time.sleep(0.01)

print("Testing MICROSTEP stepping...")
for i in range(200):
    M1.onestep(
        direction=stepper.BACKWARD,
        style=stepper.MICROSTEP)
    time.sleep(0.01)

M1.release()
print('done.')
    # time.sleep(0.01)
