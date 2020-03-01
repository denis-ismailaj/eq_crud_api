import json
from peewee import *
from instance.config import *

from playhouse.shortcuts import model_to_dict

# This is where the database goes
database = MySQLDatabase('earthquakedb', user='root', password='my-secret-pw', host=MYSQL_IP, port=MYSQL_PORT)

class BaseModel(Model):
    class Meta:
        database = database

    def stringify(self):
        return json.dumps(model_to_dict(self), default=str, sort_keys=True)

    def to_dict(self):
        return model_to_dict(self)
