#!/usr/bin/python3
"""New View for Amenity objects, handles all default RESTful API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def amenities():
    """method that returns all amenity objects"""
    list_objs = []
    objs = storage.all(Amenity)
    for obj in objs.values():
        list_objs.append(obj.to_dict())
    return jsonify(list_objs)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """method that returns a amenity obj based on id or 404"""
    objs = storage.all(Amenity)
    for obj in objs.values():
        if obj.id == amenity_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """method that deletes a amenity obj based on id or 404"""
    objs = storage.all(Amenity)
    for obj in objs.values():
        if obj.id == amenity_id:
            obj.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    """method that creates a new instance of Amenity with given data"""
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if 'name' in data.keys():
        new_obj = Amenity(**data)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """method that updates a amenity obj with given data"""
    ignore = ["id", "created_at", "updated_at"]
    target = storage.get(Amenity, amenity_id)
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
