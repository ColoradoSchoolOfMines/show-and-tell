#! /usr/bin/env python3

"""
Show and Tell
"""

from bottle import route, run, get, post, error, static_file
import kajiki
import showandtell

@route('/')
def index():
    return static_file('index.html', root='.')

run(host='localhost', port=8080, debug=True)
