#! /usr/bin/env python3

"""

"""

from bottle import route, get, post, request, redirect


@route('/user/<username>')
def user_profile(username):
    return 'Hi %s' % username


@get('/user/<username>/edit')
def show_user_edit(username):
    return 'Editing %s' % username


@post('/user/<username>/edit')
def do_user_edit(username):
    return 'Successfully edited %s' % username
