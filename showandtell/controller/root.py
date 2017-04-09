#! /usr/bin/env python3

"""
Root Controller
"""

from bottle import route, static_file
from showandtell import helpers, kajiki_view, db
import showandtell.model


@route('/')
@kajiki_view('index')
def index():
    return {'page': 'index'}

# Route all of the resources
# http://stackoverflow.com/a/13258941/2319844


@route('/resources/<filepath:path>')
def static(filepath):
    return static_file(filepath, root='resources')
