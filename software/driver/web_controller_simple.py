
from ctypes import set_errno
from time import time
import asyncio

import tornado.web
import tracemalloc
tracemalloc.start()
from pi_pico_simple import SimpleFan
last_hover =    0
last_forward =  0
last_right =    0
last_left =     0
forward_speed = 0
steer =         0

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
        forward_speed =0 
        driver.stop()
        print("ESTOP ESTOP ESTOP")


class Forward(tornado.web.RequestHandler):
    def get(self):
        global last_forward

        global driver
        global forward_speed
        if forward_speed <=90:
            forward_speed+=10
        driver.set_forward_speed(forward_speed)
        print("forward click")
        print(forward_speed)
        last_forward = time()

class Reverse(tornado.web.RequestHandler):
    def get(self):
        global last_forward
        global driver
        global forward_speed
        if forward_speed >=10:
            forward_speed-=10
        driver.set_forward_speed(forward_speed)
        print("rev click")
        print(forward_speed)
        last_forward = time()

class Right(tornado.web.RequestHandler):
    def get(self):
        global last_right
        global driver
        global steer
        if steer <= .5:
            steer +=.5
        driver.set_steering_angle(steer)
        print("right click")
        print(steer)
        last_right = time()

class Left(tornado.web.RequestHandler):
    def get(self):
        global last_left
        global steer
        if steer >= -.5:
            steer -=.5
        driver.set_steering_angle(steer)
        print("left click")
        print(steer)
        last_left = time()


class Index(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello, world")
        self.render("web_controller.html")

def make_app():
    return tornado.web.Application([
            (r"/darkmode.css",tornado.web.StaticFileHandler, {"path": "darkmode.css"},),
            (r"/", Index),
            (r"/hover/", Hover),
            (r"/0_pressed/", Estop),
            (r"/estop/", Estop),
            (r"/forward/", Forward),
            (r"/w_pressed/", Forward),
            (r"/s_pressed/", Reverse),
            (r"/a_pressed/", Left),# there will be no half a pressed with this code
            (r"/d_pressed/", Right),
            #(r"/h_pressed/", HoverToggle),
    ], debug=True)

#async def 

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
    #asyncio.create_task(app_start())
    while(1):
        print(last_forward)

if __name__ == "__main__":
    driver = SimpleFan()
    asyncio.run(main())
    #main()