#! /usr/bin/env python3

"""
User Controller
"""

import validators
import os
import functools as ft
import operator

from bottle import route, get, post, request, redirect, static_file, abort
from showandtell import db, kajiki_view, helpers, model, security_check

def can_edit(ident, user):
    admin_edit = ident.is_admin and helpers.util.from_config_yaml('admin_edit')
    return (ident and ident == user) or admin_edit

def query_user(username, edit=False):
    ident = model.Session.get_identity()
    user = db.session.query(model.Person).filter_by(multipass_username=username).first()

    if edit and not can_edit(ident, user):
        abort(403, 'You do not have permission to edit this user')

    return (user, ident)

@route('/user/<username>')
@kajiki_view('userprofile')
def user_profile(username):
    (user, ident) = query_user(username)

    if not user:
        abort(404, 'No profile found for %s' % username)

    teams = user.teams or []
    projects = [] if len(user.teams) == 0 else \
        ft.reduce(operator.add, [t.projects for t in user.teams])

    return {
        'can_edit': can_edit(ident, user),
        'teams': teams,
        'projects': projects,
        'profile': user,
        'page': 'user_profile',
    }


@post('/user/<username>/edit')
@security_check('same_user')
def do_user_edit(username):
    profile = db.session.query(model.Person)\
        .filter_by(multipass_username=username).one()

    name = request.forms.get('name')
    bio = request.forms.get('bio')
    github_username = request.forms.get('github_username')
    website = request.forms.get('website')
    profile_pic = request.files.get('profile_pic')

    if profile_pic:
        if profile_pic.filename and profile_pic.file:
            try:
                (pic, thumb) = helpers.util.upload_profile_pic(profile_pic)
            except IOError as err:
                return "{}".format(err)
            asset = model.Asset(profile_pic.filename,
                                "png", pic, thumbnail=thumb)
            profile.profile_pic = asset
            db.session.add(asset)

    if not validators.length(name, min=1):
        # TODO: Abort nicely
        abort(404, 'Bad person')

    if website and not website.startswith('http://') and not website.startswith('https://'):
        website = 'http://' + website

    if website and not validators.url(website):
        # TODO: blow up
        pass

    profile.name = name
    profile.bio = bio
    profile.github_username = github_username
    profile.website = website
    db.session.add(profile)
    db.session.commit()

    redirect('/user/%s' % username)


def get_pic(username, thumb=False):
    profile_pic = db.session.query(model.Asset)\
        .join(model.Person)\
        .filter_by(multipass_username=username).first()

    if profile_pic is None:
        # If they haven't uploaded a profile pic yet, show the default one
        return static_file('default-profile-pic.png', root='resources/images',
                           mimetype='image/png')

    # Find the file on disk and serve it up
    base_path = helpers.util.from_config_yaml('asset_save_location')
    return static_file(
        profile_pic.thumbnail if thumb and profile_pic.thumbnail else profile_pic.filename,
        root=base_path, mimetype='image/png')


@route('/user/<username>/profile_pic.png')
def profile_pic(username):
    return get_pic(username)


@route('/user/<username>/profile_thumb.png')
def profile_thumb(username):
    return get_pic(username, thumb=True)
