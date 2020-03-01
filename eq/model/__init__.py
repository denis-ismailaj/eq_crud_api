import json
from peewee import *
from instance.config import *

from playhouse.shortcuts import model_to_dict

# This is where the database goes
database = MySQLDatabase('earthquakedb', user='root', password='my-secret-pw', host=MYSQL_IP, port=MYSQL_PORT)

class BaseModel(Model):
    class Meta:
        database = database

    def stringify():
        return json.dumps(model_to_dict(self)) 

    def to_dictionary():
        return model_to_dict(self)


class Earthquake(BaseModel):
    class Meta:
        table_name = "earthquakes"

    id = PrimaryKeyField(unique = True)
    datetime = DateTimeField(db_column = "dtime")
    latitude = DoubleField(db_column = "latitude")
    longitude = DoubleField(db_column = "longitude")
    depth = DoubleField(db_column = "depth")
    position = CharField(db_column = "position") 
    magnitude = DoubleField(db_column = "magnitude")
