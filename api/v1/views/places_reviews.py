#!/usr/bin/python3
"""New View for Review objects, handles all default RESTful API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def reviews(place_id):
    """method that returns all Review objects of a Place via given state id"""
    list_objs = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    objs = storage.all(Review)
    for obj in objs.values():
        if obj.place_id == place_id:
            list_objs.append(obj.to_dict())
    return jsonify(list_objs)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """method that returns a Review obj based on id or 404"""
    objs = storage.all(Review)
    for obj in objs.values():
        if obj.id == review_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """method that deletes a Review obj based on id or 404"""
    objs = storage.all(Review)
    for obj in objs.values():
        if obj.id == review_id:
            obj.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """method that creates a new REview for a City with given data"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, "Not a JSON")
    data['place_id'] = place_id
    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")
    elif 'text' not in data.keys():
        abort(400, "Missing text")
    else:
        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)
        new_obj = Review(**data)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """method that updates a Review obj with given data"""
    ignore = ["id", "created_at", "updated_at"]
    target = storage.get(Review, review_id)
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
