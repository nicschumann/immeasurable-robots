# Immeasurable Robots

# Pinouts and Diagrams


| Rail ID | GPIO Switch Pin | MotorKit Address | Stepper Number |
|---------|-----------------|------------------|----------------|
| **A0**  | D4              | 0x60             | Stepper 1      |
| **B0**  | D17             | 0x60             | Stepper 2      |
| **C0**  | D27             | 0x61             | Stepper 1      |
| **C1**  | D14             | 0x61             | Stepper 2      |
| **B1**  | D15             | 0x62             | Stepper 1      |
| **A1**  | D18             | 0x62             | Stepper 2      |


## Stepper Motor Setup

Wire-pairs on the Adafruit stepper motors are: [`Green`, `Gray`], and [`Red`, `Yellow`]. You can test these combinations with the Continuity Test mode on a multimeter. If a wire combination lights up with some resistance, it is a pair. If there is not continuity, it is not a pair.


# Raspberry PI Setup.

## Enable I2C for Motor Control

```sh
# I2C Tools
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools

# Python Modules
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv
```

This project uses circuitpython. Install it on the pi hardware by following [this tutorial](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi).

## References

- https://circuitpython.readthedocs.io/en/2.x/shared-bindings/digitalio/__init__.html


# Sound Setup

Sound control is on an independent Raspberry Pi. The sound starts playing pn boot. It takes about 50 seconds from powering the PI to hearing sound.
