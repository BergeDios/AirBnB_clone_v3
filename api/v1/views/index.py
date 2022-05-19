#!/usr/bin/python3
"""module for index.py"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """method to reroute status page"""
    return jsonify({'status': "Ok"})
