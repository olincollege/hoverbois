from distutils.log import debug
import os
import asyncio

import tornado.web


class Hover(tornado.web.RequestHandler):
    def get(self):
        print("hover click")


class Estop(tornado.web.RequestHandler):
    def get(self):
        print("ESTOP ESTOP ESTOP")


class Forward(tornado.web.RequestHandler):
    def get(self):
        print("forward click")


class Right(tornado.web.RequestHandler):
    def get(self):
        print("right click")


class Left(tornado.web.RequestHandler):
    def get(self):
        print("left click")


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
        (r"/forward/", Forward),
        (r"/w_pressed/", Forward),
        # there will be no half a pressed with this code
        (r"/a_pressed/", Left),
        (r"/d_pressed/", Right),
        #(r"/h_pressed/", HoverToggle),
    ], debug=True)

# async def


async def app_start():
    app = make_app()
    app.listen(8888)
    while 1:
        print(asyncio.Event().is_set())
        print("fml")


def main():
    while 1:
        while asyncio.Event().is_set():
            None
        print("fml")


if __name__ == "__main__":
    asyncio.run(app_start())
    # main()
