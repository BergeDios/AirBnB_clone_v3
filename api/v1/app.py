#!/usr/bin/python3
""" module for api app"""

from flasgger import Swagger
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Flasgger",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "1.0",
            "title": "HBNB API",
            "endpoint": 'v1_views',
            "description": 'RESTFul API for HBNB',
            "route": '/v1/views',
        }
    ]
}
swagger = Swagger(app)


@app.teardown_appcontext
def teardown_db(exception):
    """method to close a session"""
    storage.close()


@app.errorhandler(404)
def errorhandler(error):
    """method to handle 404 error"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        jost = getenv('HBNB_API_HOST')
    else:
        jost = '0.0.0.0'
    if getenv('HBNB_API_PORT'):
        puerto = getenv('HBNB_API_PORT')
    else:
        puerto = 5000
    app.run(host=jost, port=puerto, threaded=True, debug=True)
