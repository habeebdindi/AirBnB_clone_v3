#!/usr/bin/python3
"""
handles all default RESTFul API actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """returns a list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """gets an review object matching the id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """deletes a review object matching the id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """creates a review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request_data.keys():
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, request_data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request_data.keys():
        return jsonify({"error": "Missing text"}), 400
    new_review = Review(place_id=place_id, user_id=request_data['user_id'],
                        text=request_data['text'])
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """updates an review object matching the id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in request_data.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
