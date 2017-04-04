#! /usr/bin/env python3

"""

"""

from bottle import route, get, post, request, redirect
from showandtell import helpers, kajiki_view


@route('/user/<username>')
@kajiki_view('userprofile')
def user_profile(username):
    return {'username': username, }


@get('/user/<username>/edit')
@kajiki_view('userprofile')
def show_user_edit(username):
    return {'username': username, 'edit': True, }


@post('/user/<username>/edit')
def do_user_edit(username):
    # TODO: Perform the edit
    redirect('/user/%s' % username)
