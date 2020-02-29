from flask import Flask

app = Flask(__name__)
# app.config.from_object('config')
# app.config.from_file('config.py')

@app.route('/')
def say_hello():
    return "Hello world"
