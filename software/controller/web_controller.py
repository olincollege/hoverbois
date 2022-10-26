from distutils.log import debug
from time import time
from time import sleep
import asyncio

import tornado.web
import tracemalloc
tracemalloc.start()

last_hover =    0
last_forward =  0
last_right =    0
last_left =     0

class Hover(tornado.web.RequestHandler):
    def get(self):
        global last_hover
        print("hover click")
        last_hover = time()


class Estop(tornado.web.RequestHandler):
    def get(self):
        print("ESTOP ESTOP ESTOP")


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

def make_app():
    return tornado.web.Application([
            (r"/darkmode.css",tornado.web.StaticFileHandler, {"path": "darkmode.css"},),
            (r"/", Index),
            (r"/hover/", Hover),
            (r"/0_pressed/", Estop),
            (r"/estop/", Estop),
            (r"/forward/", Forward),
            (r"/w_pressed/", Forward),
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
    #await app_start()
    asyncio.create_task(app_start())
    while(1):
        print(last_forward)

if __name__ == "__main__":
    
    asyncio.run(main())
    #main()