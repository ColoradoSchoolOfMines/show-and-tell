#! /usr/bin/env python3

"""
User Controller
"""

from bottle import route, get, post, request, redirect
from showandtell import db, kajiki_view, helpers
import showandtell.model


@route('/user/<username>')
@kajiki_view('userprofile')
def user_profile(username):
    user = db.session.query(showandtell.model.Person).filter_by(
        multipass_username=username)
    return {
        'profile': user.one()
    }

@post('/user/<username>/edit')
def do_user_edit(username):
    # TODO: Perform the edit
    redirect('/user/%s' % username)


@route('/user/<username>/profile_pic.jpg')
def profile_pics(username):
    profile_pic = db.session.query(showandtell.model.Asset).\
        join(showandtell.model.Person.profile_pic_id).\
        filter_by(multipass_username=username).data

    if profile_pic is None:
        # TODO: Return a default profile pic
        return None

    return profile_pic
