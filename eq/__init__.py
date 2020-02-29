from flask import Flask
from peewee import *
from instance.config import *
import json

from eq.model import database, Earthquake

from playhouse.shortcuts import model_to_dict

app = Flask(__name__)
app.config.from_pyfile("../instance/config.py")

@app.before_request
def before_request():
    database.connect()

@app.after_request
def after_request(response):
    database.close()
    return response

@app.route('/')
def say_hello():
    return "Hello world"

@app.route('/api/eq')
def get_earthquake():
    earthquakes = Earthquake.select()

    response = {
        "result": [eq.to_dictionary() for eq in earthquakedb]
    }

    return json.dumps(response), 200
