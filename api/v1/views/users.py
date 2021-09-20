#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from flask import jsonify, make_response, request, abort, Response
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def return_city():
    """return all the users"""
    users = list(storage.all(User).values())
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<string:user_id>", methods=['GET'],
                 strict_slashes=False)
def return_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete a user object"""
    users = storage.all(User)
    for key, value in users.items():
        if "User.{}".format(user_id) == key:
            storage.delete(value)
            storage.save()
            return {}
    abort(404)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a user"""
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    elif 'email' not in request.get_json():
        abort(Response("Missing email", 400))
    elif 'password' not in request.get_json():
        abort(Response("Missing password", 400))
    else:
        user = User(**request.get_json())
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201


@app_views.route("/users/<string:user_id>", methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Updates a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(Response("Not a JSON", 400))
    for key, value in body_request.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return user.to_dict(), 200
