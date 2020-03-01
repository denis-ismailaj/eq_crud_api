from flask import Flask, jsonify, request
from eq.formats import FORMATS
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

@app.route('/api/eq', methods=[ 'POST', 'GET' ])
def get_earthquake():
    if request.method == "GET":
        earthquakes = Earthquake.select()

        response = {
            "result": [eq.to_dictionary() for eq in earthquakes]
        }
        return jsonify(response)
    else: #request.method == "POST":
        # fmt = request.args.get('format')
        # if not fmt in FORMATS:
        #     return {}, 300
        if not 'file' in request.files:
            # print(dir(request))
            print(request.data)
            return "FUCK"
        format_converter = FORMATS['rss']
        f = request.files['file']
        quake = format_converter(f)
        return quake
