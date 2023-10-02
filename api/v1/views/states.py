#!/usr/bin/python3
"""
handles all default RESTFul API actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object by state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object by state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        storage.delete(city)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    """creates a state obj"""
    request_data = request.get_json()
    if request_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request_data.keys():
        return jsonify({"error": "Missing name"}), 400
    state = State(name=request_data['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """updates state"""
    state = storage.get(cls=State, id=str(state_id))
    if state is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in request_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
