__author__ = 'honhon'

class ModelFactory(object):

    def __init__(self, db, objects, get_post_put_delete, params):
        self.db = db
        self.objects = objects
        self.get_post_put_delete = get_post_put_delete
        self.params = params

    def build(self, prefix, request, args, kwargs):
        collection = self.db[prefix]
        obj = self.objects[prefix]
        params = self.params(obj._fields, args, kwargs, request.arguments)
        return self.get_post_put_delete[request.method](collection, obj, params)