#!/usr/bin/python3
"""
handles all default RESTFul API actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """returns all places objects"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """gets a place object matching the id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """deletes a place object matching the id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        storage.delete(review)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """creates an place object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data.keys():
        return jsonify({"error": "Missing user_id"}), 400
    user_id = data.get("user_id")
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    if 'name' not in data.keys():
        return jsonify({"error": "Missing name"}), 400
    new_place = Place(**data)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """updates an place object matching the id """
    data = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
