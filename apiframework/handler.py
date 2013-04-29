__author__ = 'honhon'
import tornado.web
import json
from bson import json_util

from tornado import gen

class MotorHandler(tornado.web.RequestHandler):

    def initialize(self, model, prefix, mtype):
        self.model = model
        self.prefix = prefix
        self.mtype = mtype
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

"""
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

"""

class ListHandler(MotorHandler):
    
    SUPPORTED_METHODS = ("GET")
    
    @generate_response
    def get(self, *args, **kwargs):
        self.sendJson(self.response_dict)

class PostHandler(MotorHandler):
    
    SUPPORTED_METHODS = ("POST")

    @generate_response
    def post(self, *args, **kwargs):
        self.sendJson(self.response_dict)

class FindOneHandler(MotorHandler):
    
    SUPPORTED_METHODS = ("GET")

    @generate_response
    def get(self, *args, **kwargs):
        self.sendJson(self.response_dict)

class UpdateHandler(MotorHandler):
    
    SUPPORTED_METHODS = ("PUT")

    @generate_response
    def put(self, *args, **kwargs):
        self.sendJson(self.response_dict)

class DeleteHandler(MotorHandler):

    SUPPORTED_METHODS = ("DELETE")
    
    @generate_response
    def delete(self, *args, **kwargs):
        self.sendJson(self.response_dict)

handlers = {"List": ListHandler, "Post": PostHandler, "FindOne": FindOneHandler, "Put": UpdateHandler, "Delete": DeleteHandler}

def rest_routes(objects, handlers, model):
    routes = []
    for name, cls in objects.iteritems():
        
        route = (r'/%s/list/?' % name.lower(),  handlers['List'], dict(model=model, prefix=name, mtype="list"))
        print route
        routes.append( route )
        
        route = (r'/%s/new/?' % name.lower(), handlers['Post'], dict(model=model, prefix=name, mtype="new") )
        print route
        routes.append( route )
        
        route = (r'/%s/findone/([0-9a-fA-F]{24,})/?' % name.lower(),  handlers['FindOne'], dict(model=model, prefix=name, mtype="findone"))
        print route
        routes.append( route )
        
        route = (r'/%s/update/([0-9a-fA-F]{24,})/?' % name.lower(),  handlers['Put'], dict(model=model, prefix=name, mtype="update"))
        print route
        routes.append( route )
        
        route = (r'/%s/delete/([0-9a-fA-F]{24,})/?' % name.lower(),  handlers['Delete'], dict(model=model, prefix=name, mtype="delete"))
        print route
        routes.append( route )
        
    return routes