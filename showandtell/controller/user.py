#! /usr/bin/env python3

"""
User Controller
"""

from bottle import route, get, post, request, redirect, static_file, abort
from showandtell import db, kajiki_view, helpers, model
import validators
import os


@route('/user/<username>')
@kajiki_view('userprofile')
def user_profile(username):
    user_query = db.session.query(model.Person).filter_by(
        multipass_username=username)
    
    if not user_query.first():
        abort(404, 'No profile found for %s' % username)

    user = user_query.one()

    return {
        'teams': user.teams,
        'profile': user,
        'page': 'user_profile',
    }


@post('/user/<username>/edit')
def do_user_edit(username):
    session_identity = model.Session.get_identity(request)
    if not session_identity or session_identity.multipass_username != username:
        abort(403, 'You are not allowed to edit users other than yourself')

    profile = db.session.query(model.Person)\
        .filter_by(multipass_username=username).one()

    name = request.forms.get('name')
    bio = request.forms.get('bio')
    github_username = request.forms.get('github_username')
    website = request.forms.get('website')
    profile_pic = request.files.get('profile_pic')

    if profile_pic:
        if profile_pic.filename and profile_pic.file:
            # For some reason this isn't working, just use the dumb split
            #name, ext = os.path.splittext(profile_pic.filename)
            ext = profile_pic.filename.split('.', 1)[-1]
            if ext not in ('png', 'jpg', 'jpeg', 'gif'):
                return 'File extension not allowed'

            pic_asset = model.Asset(profile_pic.filename, ext[1:],
                                    helpers.util.save_asset(profile_pic))
            profile.profile_pic = pic_asset
            db.session.add(pic_asset)

    if not validators.length(name, min=1):
        # Abort nicely
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


@route('/user/<username>/profile_pic')
def profile_pic(username):
    profile_pic = db.session.query(model.Asset)\
        .join(model.Person)\
        .filter_by(multipass_username=username).first()

    if profile_pic is None:
        # If they haven't uploaded a profile pic yet, show the default one
        return static_file('default-profile-pic.png', root='resources/images',
                           mimetype='image/png')

    # Find the file on disk and serve it up
    base_path = helpers.util.from_config_yaml('asset_save_location')
    return static_file(profile_pic.filename, root=base_path,
                       mimetype='image/%s' % profile_pic.type)
