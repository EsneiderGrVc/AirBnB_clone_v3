#!/usr/bin/python3
"""Create a estatus route"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


db_tables = {"states": State,
             "amenities": Amenity,
             "cities": City,
             "places": Place,
             "reviews": Review,
             "users": User}


@app_views.route("/status", strict_slashes=False)
def status():
    """give the API status"""
    return {'status': 'OK'}


@app_views.route("/stats", strict_slashes=False)
def count_stats():
    """endpoint that retrieves the number of each objects by type"""
    new_dict = {}
    for key, value in db_tables.items():
        new_dict[key] = storage.count(value)
    return new_dict

if __name__ == '__main__':
    pass
