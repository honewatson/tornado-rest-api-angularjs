__author__ = 'honhon'
import tornado.web
import json
from bson import json_util

from tornado import gen

class MotorHandler(tornado.web.RequestHandler):

    def initialize(self, model, prefix):
        self.model = model
        self.prefix = prefix
        self.response_dict = ""

    def sendJson(self, data):
        data = json.dumps(data, sort_keys=True, indent=4, default=json_util.default)
        self.write(data)


def generate_response(request):
    @tornado.web.asynchronous
    @gen.coroutine
    def _request(self, *args, **kwargs):

        model = self.model.build(self.prefix, self.request, args, kwargs)
        yield model.setResponseDict()
        self.response_dict = model.getResponseDict()
        gen.coroutine(request)(self, *args, **kwargs)

    return _request

class MainHandler(MotorHandler):

    @generate_response
    def get(self, *args, **kwargs):
        self.sendJson(self.response_dict)

    @generate_response
    def post(self, *args, **kwargs):
        self.sendJson(self.response_dict)

    @generate_response
    def put(self, *args, **kwargs):
        self.sendJson(self.response_dict)

    @generate_response
    def delete(self, *args, **kwargs):
        self.sendJson(self.response_dict)

def rest_routes(objects, handler, model):
    routes = []
    for name, cls in objects.iteritems():
        route = (r'/%s/?' % name.lower(), handler, dict(model=model, prefix=name) )
        print route
        routes.append( route )
        route = (r'/%s/([0-9a-fA-F]{24,})/?' % name.lower(),  MainHandler, dict(model=model, prefix=name))
        print route
        routes.append( route )
    return routes