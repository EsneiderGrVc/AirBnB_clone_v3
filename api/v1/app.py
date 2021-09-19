#!/usr/bin/python3
"""Start an API"""

import os
from models import storage
from flask import Flask, Blueprint, jsonify, make_response
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(data):
    """close"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', "0.0.0.0"),
            port=os.getenv('HBNB_API_PORT', 5000), threaded=True)
