"""
Module implementing simple web controller interface.
"""

from ctypes import set_errno
from time import time
import asyncio

import tornado.web
import tracemalloc

tracemalloc.start()

from hoverbotpy.controllers.constants import PORT

from hoverbotpy.drivers.driver_dummy import DummyHovercraftDriver
from hoverbotpy.drivers.threading_dummy import ThreadingDummy
from hoverbotpy.drivers.pi_pico_simple import SimpleFan
from hoverbotpy.drivers.pi_pico_pid import PIDCorrectedFan
import re

# Setup CLI arguments
import argparse
parser = argparse.ArgumentParser(
    prog="WebController",
    description="Web controller for PIE hovercraft.",
    epilog="Written by Joseph Gilbert and Devlin Ih",
)

parser.add_argument(
    "driver_type",
    help=("Type of driver to use. Legal values:\n"
          "  dummy, dummy_threading, pico, pico_pid"),
)

args = parser.parse_args()

# settings
MAX_FORWARD_SPEED = 60
MAX_HOVER_SPEED = 60

# Globals
# Why are these needed?
last_hover = 0
last_forward = 0
last_right = 0
last_left = 0

# Wish we were using Python 3.10 for pattern matching.
requested_driver = args.driver_type
if requested_driver == "dummy":
    driver = DummyHovercraftDriver()
elif requested_driver == "threading_dummy":
    driver = ThreadingDummy()
    driver.run_loop()
elif requested_driver == "pico":
    driver = SimpleFan("/dev/ttyACM1")
elif requested_driver == "pico_pid":
    driver = PIDCorrectedFan("/dev/ttyACM1")
    driver.run_loop()
else:
    import sys
    print(f"Error: {requested_driver} is not a valid driver type.")
    sys.exit(-1)


letter_maps = {
    'h' : driver.set_hover_speed,
    'f' : driver.set_forward_speed,
    's' : driver.set_steering_angle
}

def Drive(command: str):
    commands = command.split(", ")
    for data in commands:
        if data in letter_maps.keys():
            letter_maps[data[0]](float(data[1:-1]))
    # self.get_argument("angular_vel")
    



def main():
    while (1):
        command = input()
        Drive(command)

if __name__ == "__main__":
    # asyncio.run(main())
    main()
