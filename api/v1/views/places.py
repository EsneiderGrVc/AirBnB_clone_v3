#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from models import storage
from flask import jsonify, make_response, request, abort, Response
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<string:city_id>/places", methods=['GET'],
                 strict_slashes=False)
def return_places(city_id):
    """return all the places"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    places = []
    for place in cities.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route("/places/<string:place_id>", methods=['GET'],
                 strict_slashes=False)
def place_obj(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete a Place object"""
    places = storage.all(Place)
    for key, value in places.items():
        if "Place.{}".format(place_id) == key:
            storage.delete(value)
            storage.save()
            return {}
    abort(404)


@app_views.route("/cities/<string:city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    kwargs = request.get_json()
    if "user_id" not in kwargs:
        abort(Response("Missing user_id"), 400)
    user = storage.get(User, kwargs["user_id"])
    if user is None:
        abort(404)
    if 'name' not in kwargs:
        abort(Response("Missing name", 400))
    kwargs["city_id"] = city_id
    save_place = Place(**kwargs)
    storage.save()
    return jsonify(save_place.to_dict()), 201


@app_views.route("/places/<string:place_id>", methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(Response("Not a JSON", 400))
    for key, value in body_request.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return place.to_dict(), 200
