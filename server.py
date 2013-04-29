#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import motor

from app.config import config

define("port", default=8888, help="run on the given port", type=int)

client = motor.MotorClient().open_sync()

db = client[config['db']]


from app.objects import objects
from library.models import models, ModelParams
from library.handler import handlers
from library.handler import rest_routes


from library.factories import ModelFactory

model = ModelFactory(db, objects, models, ModelParams)

def main():
    tornado.options.parse_command_line()
    #application = tornado.web.Application(rest_routes(objects, MainHandler, model), debug=True)
    application = tornado.web.Application(rest_routes(objects, handlers, model), debug=True)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

