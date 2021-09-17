#!/usr/bin/python3
"""llenar"""

import os
from models import storage
from flask import Flask, Blueprint
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.teardown_appcontext
def teardown():
    """close"""
    storage.close()


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', "0.0.0.0"),
            port=os.getenv('HBNB_API_PORT', 5000), threaded=True)
