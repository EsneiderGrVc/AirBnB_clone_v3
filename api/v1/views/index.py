#!/usr/bin/python3
"""comment"""

from api.v1.views import app_views
from flask import Flask

app = Flask(__name__)

@app.route("/status", strict_slashes=False)
def status():
    """"""
    return {"status": "OK"}
