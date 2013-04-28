__author__ = 'honhon'
import motor
from schematics.models import Model
from schematics.serialize import (to_python, to_json, make_safe_python,
                                  make_safe_json, blacklist, whitelist)
from schematics.types import (StringType, IntType, UUIDType)
from schematics.types.mongo import ObjectIdType

class MongoModel(Model):
    _id = ObjectIdType()

class Animal(MongoModel):
    name = StringType(max_length=40)

class Machinary(MongoModel):
    name = StringType(max_length=40)

class Crops(MongoModel):
    name = StringType(max_length=40)

objects = {"Animal": Animal, "Machinary": Machinary, "Crops": Crops}

"""
curl --data "name=tractor" http://192.168.56.101:8888/machinary
curl --data "name=plough" http://192.168.56.101:8888/machinary
curl http://192.168.56.101:8888/machinary
curl http://192.168.56.101:8888/machinary/517ccd5a1d41c810a880d61e

curl --data "name=pig" http://192.168.56.101:8888/animal
curl --data "name=horse" http://192.168.56.101:8888/animal
curl --data "name=cow" http://192.168.56.101:8888/animal
curl http://192.168.56.101:8888/animal
"""