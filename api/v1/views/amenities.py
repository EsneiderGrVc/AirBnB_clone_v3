#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from flask import jsonify, make_response, request, abort, Response
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def return_amenities():
    """return all the amenities"""
    amenities = list(storage.all(Amenity).values())
    amenity_list = []
    for amenity in amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<string:amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenity_obj(amenity_id):
    """Retrieves a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete a amenity object"""
    amenities = storage.all(Amenity)
    for key, value in amenities.items():
        if "amenity.{}".format(amenity_id) == key:
            storage.delete(value)
            storage.save()
            return {}
    abort(404)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a amenity"""
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    elif 'name' not in request.get_json():
        abort(Response("Missing name", 400))
    else:
        amenity = Amenity(**request.get_json())
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(Response("Not a JSON", 400))
    for key, value in body_request.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return(jsonify(amenity.to_dict()), 200)
