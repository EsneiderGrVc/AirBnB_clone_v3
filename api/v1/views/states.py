#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from flask import jsonify, make_response, request, abort
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
