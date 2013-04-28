__author__ = 'honhon'
from schematics.types.base import DictType, GeoPointType
from schematics.types.compound import ListType, SortedListType, ModelType, MultiValueDictType
from schematics.serialize import (to_python, to_json, make_safe_python,
                                  make_safe_json, blacklist, whitelist)
from tornado import gen
import tornado.web
import functools
import motor
from schematics.validation import ValidationError
from schematics.types.mongo import ObjectIdType
from bson.objectid import ObjectId
import json

class ModelParams(object):

    def __init__(self, fields, args, kwargs, arguments):
        self.fields = fields
        self.args = args
        self.kwargs = kwargs
        self.arguments = arguments

    def getParams(self):
        types = [DictType, GeoPointType, ListType, SortedListType, ModelType, MultiValueDictType]

        fieldkeys = self.fields.keys()

        for argument, value in self.arguments.iteritems():

            if type(value) is list and argument in fieldkeys and self.fields[argument] not in types:
                self.arguments[argument] = self.arguments[argument][0]

        if len(self.args):
            self.arguments['_id'] = self.args[0]

        return self.arguments


class Model(object):

    responseDict = ""

    def __init__(self, collection, schematic, params):
        self.collection = collection
        self.schematic = schematic
        self.params = params

    def setResponseDict(self): pass

    def setResponseDictSuccess(self, result):
        self.responseDict = {"status": "Success", "result":result}

    def setResponseDictErrors(self, errors):
        self.responseDict = {"status": "Errors",  "errors": errors}


    def getIdDict(self, _id):
        return {"_id":ObjectId(_id)}

    def getResponseDict(self):
        return self.responseDict

        """
            model.collection
            model.schematic
            model.parameters


            model.schematic(**model.parameters)
            if model.schematic().validate():
                response = model.collection.doaction(model.schematic)
            else
                response =
            response logic
        """

class GetModel(Model):

    @gen.coroutine
    def setResponseDict(self):
        params = self.params.getParams()
        if len(params):
            try:
                result = yield motor.Op( self.collection.find_one, self.getIdDict(params['_id']) )
                result['_id'] = str(result['_id'])

                self.setResponseDictSuccess(result)
            except Exception, e:

                self.setResponseDictErrors("Not Found!")
        else:
            cursor = self.collection.find().sort([('_id', -1)])
            results = {str(document['_id']):document for document in (yield motor.Op(cursor.to_list))}
            #results = [document for document in (yield motor.Op(cursor.to_list))]
            self.setResponseDictSuccess(results)
        return
        #obj = self.schematic(**params)
        #import pdb; pdb.set_trace()


class PostModel(Model):

    @gen.coroutine
    def setResponseDict(self):
        params = self.params.getParams()
        obj = self.schematic(**params)
        try:
            obj.validate()
            result = yield motor.Op(self.collection.save, to_python(obj))
            self.setResponseDictSuccess({"_id": str(result)})
        except ValidationError, e:
            self.setResponseDictErrors(e)
        return

#TODO put
class PutModel(Model):
    def getResponseDict(self): pass

class DeleteModel(Model):


    @gen.coroutine
    def setResponseDict(self):
        params = self.params.getParams()

        try:
            result = yield motor.Op(self.collection.remove, self.getIdDict(params['_id']))
            self.setResponseDictSuccess({"_id": str(result)})
        except ValidationError, e:
            self.setResponseDictErrors(e)
        return

models = {"GET": GetModel, "POST": PostModel, "PUT": PostModel, "DELETE": DeleteModel}


"""
def save_action(request):

    @functools.wraps(request)
    @gen.coroutine
    def _save_action(self):
        params = self.params.getParams()
        params['name'] = 1
        obj = self.schematic(**params)
        try:
            obj.validate()
            result = yield motor.Op(self.collection.save, to_python(obj))

            self.setResponseDictSuccess({"_id": result})
        except ValidationError, e:
            self.setResponseDictErrors(e)
        gen.coroutine(request)(self)

    return _save_action
"""
