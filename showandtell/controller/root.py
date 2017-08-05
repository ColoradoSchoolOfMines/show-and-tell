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


@route('/schedule')
@kajiki_view('schedule')
def schedule():
    return {'page': 'schedule'}


@route('/mailinglist')
@kajiki_view('mailing_list')
def mailing_list():
    return {'page': 'mailing_list'}


@route('/contact')
@kajiki_view('contact')
def contact():
    return {'page': 'contact'}


@route('/resources/<filepath:path>')
def static(filepath):
    """
    Routes all of the resources
    http://stackoverflow.com/a/13258941/2319844
    """
    return static_file(filepath, root='resources')
