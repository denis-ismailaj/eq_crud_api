from peewee import *
from playhouse.shortcuts import model_to_dict

from . import BaseModel

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
