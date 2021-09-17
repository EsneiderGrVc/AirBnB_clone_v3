#!/usr/bin/python3
"""Create a estatus route"""

from api.v1.views import app_views
from flask import Flask


@app_views.route("/status", strict_slashes=False)
def status():
    """give the API status"""
    return {'status': 'OK'}
