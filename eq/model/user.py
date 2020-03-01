from peewee import *
from playhouse.shortcuts import model_to_dict

from . import BaseModel

class User(BaseModel):
    class Meta:
        table_name = "users"

    id = PrimaryKeyField(unique = True)

    username = CharField()
    email = CharField()
    password = CharField()
