#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from flask import jsonify, make_response, request, abort, Response
from werkzeug.wrappers import response
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route("/states", strict_slashes=False)
def return_states():
    """return all the states"""
    states = list(storage.all(State).values())
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<string:state_id>", strict_slashes=False)
def state_obj(state_id):
    """Retrieves a State object"""
    if state_id is not None:
        return(storage.get(State, state_id).to_dict())
    else:
        abort(404)


@app_views.route("/states/<string:state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete a state object"""
    states = storage.all(State)
    for key, value in states.items():
        if "State.{}".format(state_id) == key:
            storage.delete(value)
            storage.save()
            return {}
    abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State"""
    if not request.get_json():
        return abort(Response("Not a JSON", 400))
    elif 'name' not in request.get_json():
        return abort(Response("Missing name", 400))
    else:
        state = State(**request.get_json())
        storage.new(state)
        storage.save()
        return state.to_dict(), 201


@app_views.route("/states/<string:state_id>", methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(Response("Not a JSON", 400))
    for key, value in body_request.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return state.to_dict(), 200
