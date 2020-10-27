# Immeasurable Robots


## Stepper Motor Setup

- Wire-pairs on the Adafruit stepper motors are: [`Green`, `Gray`], and [`Red`, `Yellow`]. You can test these combinations with the Continuity Test mode on a multimeter. If a wire combination lights up with some resistance, it is a pair. If there is not continuity, it is not a pair.

## References

- https://circuitpython.readthedocs.io/en/2.x/shared-bindings/digitalio/__init__.html



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
