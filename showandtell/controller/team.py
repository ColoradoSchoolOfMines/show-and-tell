#! /usr/bin/env python3

"""
Team Controller
"""

from bottle import route, get, post, request, redirect, static_file, abort
from showandtell import db, kajiki_view, helpers, model
import validators
import os

@route('/team/<id>')
@kajiki_view('team')
def team_profile(id):

@get('/team/new')
@kajiki_view('team')
def team_profile_new():

@post('/team/new')
def team_profile_new():


@post('/team/<id>/edit')
def do_edit_team(id):