from peewee import *
from playhouse.shortcuts import model_to_dict

from . import BaseModel
from . user import User
from . earthquake import Earthquake

class SurveyField(BaseModel):
    id = PrimaryKeyField(unique = True)

    earthquake = ForeignKeyField(Earthquake)
    input_type = IntegerField()
    title = CharField()
    choice = TextField()

class SurveySubmission(BaseModel):
    id = PrimaryKeyField(unique = True)

    created_at = DateTimeField()
    created_by = ForeignKeyField(User, null = True)

class SurveyAnswer(BaseModel):
    id = PrimaryKeyField(unique = True)

    field = ForeignKeyField(SurveyField)
    value = CharField()
    submission = ForeignKeyField(SurveySubmission)
