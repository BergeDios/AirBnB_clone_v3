#!/usr/bin/python3
"""New View for User objects, handles all default RESTful API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.user import User


@app_views.route("/users", methods=['GET'],
                 strict_slashes=False)
def users():
    """method that returns all user objects"""
    list_objs = []
    objs = storage.all(User)
    for obj in objs.values():
        list_objs.append(obj.to_dict())
    return jsonify(list_objs)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """method that returns a User obj based on id or 404"""
    objs = storage.all(User)
    for obj in objs.values():
        if obj.id == user_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """method that deletes a User obj based on id or 404"""
    objs = storage.all(User)
    for obj in objs.values():
        if obj.id == user_id:
            obj.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/users", methods=['POST'],
                 strict_slashes=False)
def post_user():
    """method that creates a new User obj with given data"""
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if 'email' not in data.keys():
        abort(400, "Missing email")
    elif 'password' not in data.keys():
        abort(400, "Missing password")
    else:
        new_obj = User(**data)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """method that updates a User obj with given data"""
    ignore = ["id", "created_at", "updated_at"]
    target = storage.get(User, user_id)
    data = request.get_json(force=True, silent=True)
    if target is None:
        abort(404)
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ignore:
            setattr(target, key, value)
    storage.save()
    return jsonify(target.to_dict()), 200
