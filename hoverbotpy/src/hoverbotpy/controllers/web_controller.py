import threading
from time import time
from time import sleep
import asyncio

import tornado.web
import tracemalloc

from hoverbotpy.controllers.constants import PORT

from hoverbotpy.drivers.driver_dummy import DummyHovercraftDriver
from hoverbotpy.drivers.threading_dummy import ThreadingDummy
from hoverbotpy.drivers.pi_pico_simple import SimpleFan
from hoverbotpy.drivers.pi_pico_pid import PIDCorrectedFan

tracemalloc.start()

TIMEOUT_TIME = .5  # IDK UNITS
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
        if driver.hover>0:
            driver.set_hover_speed(0)
        else:
            driver.set_hover_speed(20)
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
        driver.set_forward_speed(60)
        print("forward click")
        print(driver.forward)
        last_forward = time()


class NotForward(tornado.web.RequestHandler):
    def get(self):
        global last_forward
        global driver
        driver.set_forward_speed(0)
        print("not forward click")
        print(driver.forward)
        last_forward = time()


class Reverse(tornado.web.RequestHandler):
    def get(self):
        global last_forward
        global driver
        driver.set_forward_speed(0)
        print("rev click")
        print(driver.forward)
        #last_forward = time()#'''


class Right(tornado.web.RequestHandler):
    def get(self):
        global last_right
        global driver
        driver.set_steering_angle(-.75)
        print("right click")
        print(driver.steering)
        last_right = time()


class NotRight(tornado.web.RequestHandler):
    def get(self):
        global last_right
        global driver
        driver.set_steering_angle(0)
        print("not right click")
        print(driver.steering)
        last_right = time()


class Left(tornado.web.RequestHandler):
    def get(self):
        global last_left
        global driver
        driver.set_steering_angle(.75)
        print("left click")
        print(driver.steering)
        last_left = time()


class NotLeft(tornado.web.RequestHandler):
    def get(self):
        global last_left
        global driver
        driver.set_steering_angle(0)
        print("not left click")
        print(driver.steering)
        last_left = time()


class Index(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello, world")
        self.render("web_controller.html")

    def on_connection_close(self):
        print("connection closed")


def make_app():  # might be better to use a websocket in future versions
    return tornado.web.Application([
        (r"/darkmode.css", tornado.web.StaticFileHandler,
         {"path": "darkmode.css"},),
        (r"/", Index),
        (r"/hover/", Hover),
        (r"/0_pressed/", Estop),
        (r"/estop/", Estop),
        (r"/forward/", Forward),
        (r"/w_pressed/", Forward),
        # there will be no half a pressed with this code
        (r"/a_pressed/", Left),
        (r"/d_pressed/", Right),
        (r"/w_released/", NotForward),
        # there will be no half a pressed with this code
        (r"/a_released/", NotLeft),
        (r"/d_released/", NotRight),
        #(r"/h_pressed/", HoverToggle),
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


class WatchdogThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):

        print("watchdog thread started")
        running = True
        while running:
            now = time()
            # print(now)
            if ((last_forward + TIMEOUT_TIME) < now) and driver.forward != 0:
                print("forward timeout")
                driver.set_forward_speed(0)
            if (((last_left + TIMEOUT_TIME) < now) or ((last_right + TIMEOUT_TIME) < now))and driver.steering != 0:
                print("turn timeout")
                driver.set_steering_angle(0)



from hoverbotpy.drivers.driver_dummy import DummyHovercraftDriver


if __name__ == "__main__":
    driver = DummyHovercraftDriver()
    motor_watchdog_thread = WatchdogThread(1, "watchdog_1", 1)
    motor_watchdog_thread.setDaemon(True)
    motor_watchdog_thread.start()
    asyncio.run(app_start())
