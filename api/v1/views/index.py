#!/usr/bin/python3
"""module for index.py"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    """method to reroute status page"""
    return jsonify(status="Ok")

@app_views.route("/stats")
def stats():
    """method that returns dictionary containing every class count"""
    return jsonify(amenities=storage.count("Amenities"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
