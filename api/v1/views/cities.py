#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from flask import jsonify, make_response, request, abort, Response
from api.v1.views import app_views
from models.state import State
from models import storage
from models.city import City


@app_views.route("/states/<string:state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def return_cities(state_id):
    """return all the cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<string:city_id>", methods=['GET'],
                 strict_slashes=False)
def cities_obj(city_id):
    """Retrieves a State object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """delete a city object"""
    cities = storage.all(City)
    for key, value in cities.items():
        if "City.{}".format(city_id) == key:
            storage.delete(value)
            storage.save()
            return {}
    abort(404)


@app_views.route("/states/<string:state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    if 'name' not in request.get_json():
        abort(Response("Missing name", 400))
    city = request.get_json()
    city["state_id"] = state_id
    save_city = City(**city)
    storage.save()
    return jsonify(save_city.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(Response("Not a JSON", 400))
    for key, value in body_request.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return city.to_dict(), 200
