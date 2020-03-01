from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from peewee import *
from instance.config import *
import json

from eq.model import database 
from eq.model.earthquake import Earthquake
from eq.util import ts_to_dt
from eq.formats import FORMATS
from eq.util.exceptions import ApiError, BadParamError
from eq.hooks import post_notify
from eq.auth import identity, authenticate_username
from flask import Flask, jsonify, request

from flask_jwt import JWT, jwt_required, current_identity

from peewee import *
from instance.config import *
import json

from eq.model import database 
from eq.model.earthquake import Earthquake
from eq.model.survey import *
from eq.util import ts_to_dt
from eq.formats import FORMATS
from eq.util.exceptions import ApiError, BadParamError
from eq.hooks import post_notify
from eq.auth import identity, authenticate_username

from playhouse.shortcuts import model_to_dict

app = Flask(__name__)

app.config.from_pyfile("../instance/config.py")
# jwt = JWT(app, authenticate_username, identity)

##

@app.before_request
def before_request():
    database.connect()

@app.after_request
def after_request(response):
    response.headers["Access-Control-ALlow-Origin"] = "*"
    database.close()
    return response

@app.errorhandler(ApiError)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code 
    return response 

# jwt = JWT(app, authenticate_username, identity)

##
##

@app.route('/')
def say_hello():
    return "Hello world"

@app.route('/api/eq', methods=[ 'POST', 'GET' ])
def get_earthquakes():
    """GET:Get earthquakes, ordered by datetime, paginated, and with 
    some additional querying parameters

    POST: Upload a specific file format (specified by the format query
    parameter), which is then parsed, and eventually inserted into the 
    database"""

    if request.method == "GET":
        page, per_page = 1, 10

        #We do the filtering here, in a not so nice way:
        filters = [True]
        if "from" in request.args:
            _from = ts_to_dt(request.args.get("from"))
            if not _from:
                raise BadParamError("from")
            filters.append(Earthquake.datetime >= _from)

        if "to" in request.args:
            _to = ts_to_dt(request.args.get("to"))
            if not _to:
                raise BadParamError("to")
            filters.append(Earthquake.datetime <= _to)

        if "location" in request.args:
            _location = request.args.get("location")
            filters.append(Earthquake.position.contains(_location))

        if "page" in request.args:
            _page = request.args.get("page")
            if not _page.isdigit():
                raise BadParamError("page")
            page = int(_page)

        if "per_page" in request.args:
            _per_page = request.args.get("per_page")
            if not _per_page.isdigit():
                raise BadParamError("per_page")

            _per_page = int(_per_page)
            if _per_page > 20:
                raise BadParamError("per_page", {"explanation": "At most 20 page elements"})

            per_page = int(_per_page)

        earthquakes = Earthquake \
            .select() \
            .where(*filters) \
            .order_by(Earthquake.datetime.desc()) \
            .paginate(page, per_page)

        response = {
            "result": [eq.to_dict() for eq in earthquakes],
            "page": page,
            "per_page": per_page
        }

        return jsonify(response)

    else: #request.method == "POST":
        fmt = request.args.get('format')
        if not fmt in FORMATS:
            return {}, 300
        if not 'file' in request.files:
            # print(dir(request))
            print(request.data)
            return "FUCK"
        format_converter = FORMATS['rss']
        f = request.files['file']
        quake = format_converter(f)
        return quake

@app.route('/api/protected', methods=['GET'])
# @jwt_required()
def protected():
    return "" % current_identity, 200

@app.route('/api/survey/field', methods=['GET'])
def get_survey_fields():
    fields = SurveyField \
        .select() \

    return jsonify([field.to_dict() for field in fields])

@post_notify
@app.route('/api/eq/<id>')
def get_earthquake(id):
    earthquake = Earthquake \
        .select() \
        .where(Earthquake.id == id) \
        .first()

    if not earthquake:
        raise ApiError("Earthquake doesn't exist", 404)

    return jsonify(earthquake.to_dict())
