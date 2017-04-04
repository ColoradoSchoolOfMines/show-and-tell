#! /usr/bin/env python3

"""
Root Controller
"""

from bottle import route
from showandtell import helpers, kajiki_view


@route('/')
@kajiki_view('index')
def index():
    return {'page': 'index'}
