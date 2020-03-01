from peewee import *
from playhouse.shortcuts import model_to_dict

from . import BaseModel
from . user import User

class Survey(BaseModel):
    id = PrimaryKeyField(unique = True)

    title = CharField()
    created = DateTimeField()
    json_schema = TextField()

    created_by = ForeignKeyField(User, null=True)
    #A one to many relationship with SurveyQuestion

class SurveyField(BaseModel):
    id = PrimaryKeyField(unique = True)

    label = CharField()

    survey = ForeignKeyField(Survey)

class FilledSurvey(BaseModel):
    id = PrimaryKeyField(unique = True)

    survey = ForeignKeyField(Survey)
    filled_by = ForeignKeyField(User, null=True)

class FilledSurveyField(BaseModel):
    id = PrimaryKeyField(unique = True)

    filled_survey = ForeignKeyField(FilledSurvey)
