#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from flask import jsonify, make_response, request, abort, Response
from api.v1.views import app_views
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route("/places/<string:place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def return_review(place_id):
    """return all the reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route("/reviews/<string:review_id>", methods=['GET'],
                 strict_slashes=False)
def review_obj(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("reviews/<string:review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a Review object"""
    reviews = storage.all(Review)
    for key, value in reviews.items():
        if "Review.{}".format(review_id) == key:
            storage.delete(value)
            storage.save()
            return {}
    abort(404)


@app_views.route("/places/<string:place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    kwargs = request.get_json()
    if "user_id" not in kwargs:
        abort(Response("Missing user_id", 400))
    user = storage.get(User, kwargs["user_id"])
    if user is None:
        abort(404)
    if 'text' not in kwargs:
        abort(Response("Missing text", 400))
    kwargs["place_id"] = place_id
    save_review = Review(**kwargs)
    storage.save()
    return jsonify(save_review.to_dict()), 201


@app_views.route("/reviews/<string:review_id>", methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Updates a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(Response("Not a JSON", 400))
    for key, value in body_request.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return review.to_dict(), 200
