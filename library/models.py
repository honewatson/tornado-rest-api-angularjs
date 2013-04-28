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
        """
        Check the schematic object to see if arguments from Tornado can be lists or dictionaries
        """
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

    def setResponseDict(self):

        """
            Main logic for request is performed here
            self.collection ( mongo collection )
            self.schematic ( schematic model )
            self.params ( ModelParams )
            Nothing is returned because generally a coroutine and yield statement is used.
        """

    def setResponseDictSuccess(self, result):
        self.responseDict = {"status": "Success", "result":result}

    def setResponseDictErrors(self, errors):
        self.responseDict = {"status": "Errors",  "errors": errors}

    def getIdDict(self, _id):
        return {"_id":ObjectId(_id)}

    def getResponseDict(self):
        return self.responseDict


class GetModel(Model):

    @gen.coroutine
    def setResponseDict(self):
        """
        Either send get a single result if there is an _id parameter or send a list of results
        """
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
            self.setResponseDictSuccess(results)
        return

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

