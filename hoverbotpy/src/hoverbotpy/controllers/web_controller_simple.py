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
    driver = SimpleFan()
elif requested_driver == "pico_pid":
    driver = PIDCorrectedFan()
    driver.run_loop()
else:
    import sys
    print(f"Error: {requested_driver} is not a valid driver type.")
    sys.exit(-1)


class Hover(tornado.web.RequestHandler):
    def get(self):
        global driver
        global last_hover
        print("hover click")
        last_hover = time()
        speed = driver.hover
        speed = min(speed+5,40)
        driver.set_hover_speed(speed)
        
        '''
        if driver.hover>0:
            driver.set_hover_speed(0)
        else:
            driver.set_hover_speed(35)#'''
        pass


class Estop(tornado.web.RequestHandler):
    def get(self):
        global driver
        driver.stop()
        print("ESTOP ESTOP ESTOP")


class Forward(tornado.web.RequestHandler):
    def get(self):
        global last_forward
        global driver
        forward_speed = driver.forward
        if forward_speed <= 40:
            forward_speed += 5
        driver.set_forward_speed(forward_speed)
        print(f"forward click, forward speed: {forward_speed}")
        last_forward = time()


class Reverse(tornado.web.RequestHandler):
    def get(self):
        global last_forward
        global driver
        forward_speed = driver.forward
        if forward_speed >= 10:
            forward_speed -= 10
        driver.set_forward_speed(forward_speed)
        print(f"reverse click, forward speed: {forward_speed}")
        last_forward = time()


class Right(tornado.web.RequestHandler):
    def get(self):
        global last_right
        global driver
        steer = driver.steering
        if steer >= -.5:
            steer -= .5
        driver.set_steering_angle(steer)
        print(f"right click, steer {steer}")
        last_right = time()


class Left(tornado.web.RequestHandler):
    def get(self):
        global last_left
        global driver
        steer = driver.steering
        if steer <= .5:
            steer += .5
        driver.set_steering_angle(steer)
        print(f"left click,  steer{steer}")
        last_left = time()


class DecreaseErr(tornado.web.RequestHandler):
    def get(self):
        global driver

        try:
            prop_err = driver.prop_err
            if prop_err >= -1.0:
                prop_err -= .01
            driver.set_steering_angle(0)
            print(f"decrease prop_err: {prop_err}")
        except:
            print("This is not a PID controller.")


class IncreaseErr(tornado.web.RequestHandler):
    def get(self):
        global driver

        try:
            prop_err = driver.prop_err
            if prop_err <= 1.0:
                prop_err += .01
            driver.set_steering_angle(0)
            print(f"increase prop_err: {prop_err}")
        except:
            print("This is not a PID controller.")


class DecreaseDdx(tornado.web.RequestHandler):
    def get(self):
        global driver

        try:
            prop_ddt = driver.prop_ddt
            if prop_ddt >= -1:
                prop_ddt -= .01
            #driver.set_steering_angle(steer)
            print(f"decrease prop_ddt: {prop_ddt}")
        except:
            print("This is not a PID controller.")


class IncreaseDdx(tornado.web.RequestHandler):
    def get(self):
        global driver

        try:
            prop_ddx = driver.prop_ddt
            if prop_ddx <= 1:
                prop_ddx += .01
            #driver.set_steering_angle(steer)
            print(f"increase prop_ddto: {prop_ddx}")
        except:
            print("This is not a PID controller.")


class Index(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello, world")
        self.render("web_controller.html")


def make_app():
    return tornado.web.Application([
        (r"/darkmode.css", tornado.web.StaticFileHandler,
         {"path": "darkmode.css"},),
        (r"/", Index),
        (r"/hover/", Hover),
        (r"/0_pressed/", Estop),
        (r"/estop/", Estop),
        (r"/%20_pressed/", Estop),
        (r"/forward/", Forward),
        (r"/w_pressed/", Forward),
        (r"/s_pressed/", Reverse),
        # there will be no half a pressed with this code
        (r"/a_pressed/", Left),
        (r"/d_pressed/", Right),
        (r"/h_pressed/", Hover),
        (r"/i_pressed/", IncreaseDdx),
        (r"/k_pressed/", DecreaseDdx),
        (r"/o_pressed/", IncreaseErr),
        (r"/l_pressed/", DecreaseErr),

        # Manually calibrate PID controller

        # DecreaseErr, IncreaseErr, DecreaseDdx, IncreaseDdx

        # TODO: Make this work, I don't get the html stuff (I tried adding to
        # the charlist).
    ], debug=True)

# async def


async def app_start():
    app = make_app()
    app.listen(PORT)
    await asyncio.Event().wait()


async def web_app():
    print("web server start")
    app = make_app()
    app.listen(PORT)


def main():
    asyncio.run(app_start())
    # while (1):
    #     print(last_forward)

if __name__ == "__main__":
    # asyncio.run(main())
    main()
