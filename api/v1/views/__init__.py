#!/usr/bin/python3
"""comment"""

from api.v1.views.index import *
from flask import Blueprint


app_views = Blueprint('app_views', __name__, template_folder='/api/v1')
