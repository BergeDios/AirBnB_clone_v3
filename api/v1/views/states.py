#!/usr/bin/python3
"""New View for state objects, handles all default RESTful API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states():
    """method that returns all state objects"""
    list_objs = []
    objs = storage.all(State)
    for obj in objs.values():
        list_objs.append(obj.to_dict())
    return jsonify(list_objs)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """method that returns a state obj based on id or 404"""
    objs = storage.all(State)
    for obj in objs.values():
        if obj.id == state_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """method that deletes a state obj based on id or 404"""
    objs = storage.all(State)
    for obj in objs.values():
        if obj.id == state_id:
            obj.delete()
            return jsonify({}), 200
    abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    """method that creates a new instance of State with given data"""
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if 'name' in data.keys():
        new_obj = State(**data)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """method that updates a state obj with given data"""
    target = storage.get(State, state_id)
    data = request.get_json(force=True, silent=True)
    if target is None:
        abort(404)
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key != id or key != created_at or key != updated_at:
            setattr(target, key, value)
    storage.save()
    return jsonify(target.to_dict()), 200
