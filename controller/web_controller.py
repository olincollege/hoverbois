#from flask import Flask

#app = Flask(__name__)

#@app.route("/flask")
#def hello_world():
#    return "<p>Hello, World!</p>"

import asyncio

import tornado.web


class hover(tornado.web.RequestHandler):
    def get(self):
        print("hover click")


class estop(tornado.web.RequestHandler):
    def get(self):
        print("ESTOP ESTOP ESTOP")


class forward(tornado.web.RequestHandler):
    def get(self):
        print("forward click")

class not_forward(tornado.web.RequestHandler):
    def get(self):
        print("forward un click")

class left(tornado.web.RequestHandler):
    def get(self):
        print("left click")

class not_left(tornado.web.RequestHandler):
    def get(self):
        print("left un click")

class Index(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello, world")
        self.render("web_controller.html")

def make_app():
    return tornado.web.Application([
            (r"/", Index),
            (r"/hover/", hover),
            (r"/estop/", estop),
            (r"/forward/", forward),
            (r"/w_down/", forward),
            (r"/w_up/", not_forward),
            (r"/a_down/", left),
            (r"/a_up/", not_left),
    ])

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())