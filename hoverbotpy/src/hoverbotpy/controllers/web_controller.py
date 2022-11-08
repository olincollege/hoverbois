import threading
from distutils.log import debug
from time import time
from time import sleep
import asyncio

import tornado.web
import tracemalloc

from hoverbotpy.drivers.pi_pico_simple import SimpleFan
from hoverbotpy.controllers.constants import PORT

tracemalloc.start()

last_hover = 0
last_forward = 0
last_right = 0
last_left = 0
TIMEOUT_TIME = .5  # IDK UNITS


class Hover(tornado.web.RequestHandler):
    def get(self):
        global last_hover
        print("hover click")
        last_hover = time()


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
        print(forward_speed)
        last_forward = time()


class NotForward(tornado.web.RequestHandler):
    def get(self):
        global last_forward

        global driver
        driver.set_forward_speed(0)
        print("forward click")
        print(forward_speed)
        last_forward = time()


class Reverse(tornado.web.RequestHandler):
    def get(self):
        global last_forward
        global driver
        driver.set_forward_speed(0)
        print("rev click")
        print(forward_speed)
        last_forward = time()#'''


class Right(tornado.web.RequestHandler):
    def get(self):
        global last_right
        global driver
        driver.set_steering_angle(-.75)
        print("right click")
        print(steer)
        last_right = time()


class NotRight(tornado.web.RequestHandler):
    def get(self):
        global last_right
        global driver
        driver.set_steering_angle(0)
        print("right click")
        print(steer)
        last_right = time()


class Left(tornado.web.RequestHandler):
    def get(self):
        global last_left
        global driver
        driver.set_steering_angle(.75)
        print("left click")
        print(steer)
        last_left = time()


class NotLeft(tornado.web.RequestHandler):
    def get(self):
        global last_left
        global driver
        driver.set_steering_angle(0)
        print("left click")
        print(steer)
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
            if ((last_forward + TIMEOUT_TIME) < now) and forward_speed != 0:
                print("forward timeout")
                driver.set_forward_speed(0)
            if (((last_left + TIMEOUT_TIME) < now) or ((last_right + TIMEOUT_TIME) < now))and steer != 0:
                print("turn timeout")
                driver.set_steering_angle(0)



from hoverbotpy.drivers.driver_dummy import DummyHovercraftDriver


if __name__ == "__main__":
    driver = DummyHovercraftDriver()
    motor_watchdog_thread = WatchdogThread(1, "watchdog_1", 1)
    motor_watchdog_thread.setDaemon(True)
    motor_watchdog_thread.start()
    asyncio.run(app_start())
