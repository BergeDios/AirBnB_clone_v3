#!/usr/bin/python3
"""module for index.py"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """method to reroute status page"""
    return jsonify(status="OK")


@app_views.route("/stats")
def stats():
    """method that returns dictionary containing every class count"""
    return jsonify(amenities=storage.count(Amenity),
                   cities=storage.count(City),
                   places=storage.count(Place),
                   reviews=storage.count(Review),
                   states=storage.count(State),
                   users=storage.count(User))
