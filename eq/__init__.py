from flask import Flask
from peewee import *
from instance.config import *

app = Flask(__name__)
app.config.from_pyfile("../instance/config.py")


@app.route('/')
def say_hello():
    return "Hello world"

