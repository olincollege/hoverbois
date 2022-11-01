import threading
from distutils.log import debug
from time import time
from time import sleep
import asyncio

import tornado.web
import tracemalloc

from hoverbotpy.drivers.pi_pico_simple import SimpleFan

tracemalloc.start()

last_hover = 0
last_forward = 0
last_right = 0
last_left = 0
forward_speed = 0
steer = 0
TIMEOUT_TIME = .5  # IDK UNITS


class Hover(tornado.web.RequestHandler):
    def get(self):
        global last_hover
        print("hover click")
        last_hover = time()


class Estop(tornado.web.RequestHandler):
    def get(self):
        global driver
        global steer
        global forward_speed
        steer = 0
        forward_speed = 0
        driver.stop()
        print("ESTOP ESTOP ESTOP")


class Forward(tornado.web.RequestHandler):
    def get(self):
        global last_forward

        global driver
        global forward_speed
        if forward_speed <= 90:
            forward_speed += 10
        driver.set_forward_speed(forward_speed)
        print("forward click")
        print(forward_speed)
        last_forward = time()


class Reverse(tornado.web.RequestHandler):
    def get(self):
        global last_forward
        global driver
        global forward_speed
        if forward_speed >= 10:
            forward_speed -= 10
        driver.set_forward_speed(forward_speed)
        print("rev click")
        print(forward_speed)
        last_forward = time()


class Right(tornado.web.RequestHandler):
    def get(self):
        global last_right
        global driver
        global steer
        if steer >= -.5:
            steer -= .5
        driver.set_steering_angle(steer)
        print("right click")
        print(steer)
        last_right = time()


class Left(tornado.web.RequestHandler):
    def get(self):
        global last_left
        global steer
        if steer <= .5:
            steer += .5
        driver.set_steering_angle(steer)
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
    app.listen(8888)
    await asyncio.Event().wait()


async def web_app():
    print("web server start")
    app = make_app()
    app.listen(8888)


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
            if ((last_forward + TIMEOUT_TIME) < now):
                print("forward timeout")
            if ((last_left + TIMEOUT_TIME) < now) or ((last_right + TIMEOUT_TIME) < now):
                print("turn timeout")



from hoverbotpy.drivers.driver_dummy import DummyHovercraftDriver


if __name__ == "__main__":
    driver = DummyHovercraftDriver()
    motor_watchdog_thread = WatchdogThread(1, "watchdog_1", 1)
    motor_watchdog_thread.setDaemon(True)
    motor_watchdog_thread.start()
    asyncio.run(app_start())
