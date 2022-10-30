import threading
from distutils.log import debug
from time import time
from time import sleep
import asyncio

import tornado.web
import tracemalloc
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
        print("ESTOP ESTOP ESTOP")


class NotForward(tornado.web.RequestHandler):
    def get(self):
        global last_forward
        print("forward click release")
        last_forward = time()


class NotRight(tornado.web.RequestHandler):
    def get(self):
        global last_right
        print("right click release")
        last_right = time()


class NotLeft(tornado.web.RequestHandler):
    def get(self):
        global last_left
        print("left click release")
        last_left = time()


class Forward(tornado.web.RequestHandler):
    def get(self):
        global last_forward
        print("forward click")
        last_forward = time()


class Right(tornado.web.RequestHandler):
    def get(self):
        global last_right
        print("right click")
        last_right = time()


class Left(tornado.web.RequestHandler):
    def get(self):
        global last_left
        print("left click")
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


async def main():
    await app_start()
    # asyncio.create_task(app_start())
    while (1):
        print(last_forward)


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


if __name__ == "__main__":
    motor_watchdog_thread = WatchdogThread(1, "watchdog_1", 1)
    motor_watchdog_thread.setDaemon(True)
    motor_watchdog_thread.start()
    asyncio.run(app_start())
    # main()
