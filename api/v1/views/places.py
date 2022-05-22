#!/usr/bin/python3
"""New View for Place objects, handles all default RESTful API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """method that returns all Place objects of a City via given state id"""
    list_objs = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    objs = storage.all(Place)
    for obj in objs.values():
        if obj.city_id == city_id:
            list_objs.append(obj.to_dict())
    return jsonify(list_objs)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """method that returns a Place obj based on id or 404"""
    objs = storage.all(Place)
    for obj in objs.values():
        if obj.id == place_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """method that deletes a Place obj based on id or 404"""
    objs = storage.all(Place)
    for obj in objs.values():
        if obj.id == place_id:
            obj.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """method that creates a new Place for a City with given data"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, "Not a JSON")
    data['city_id'] = city_id
    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")
    elif 'name' not in data.keys():
        abort(400, "Missing name")
    else:
        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)
        new_obj = Place(**data)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """method that updates a Place obj with given data"""
    ignore = ["id", "created_at", "updated_at"]
    target = storage.get(Place, place_id)
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
