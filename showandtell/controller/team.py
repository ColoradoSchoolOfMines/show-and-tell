#! /usr/bin/env python3

"""
Team Controller
"""

from bottle import route, get, post, request, redirect, static_file, abort
from showandtell import db, kajiki_view, helpers, model
import validators
import os

@route('/team/<ident>')
@kajiki_view('team')
def team_profile(ident):
    user = model.Session.get_identity(request)
    team_result = db.session.query(model.Team).filter_by(
        team_id=ident)

    if not team_result.first():
        abort(404, 'No profile found for team #%s' % ident)

    team = team_result.one()

    return {
        'team': team,
        'is_new': False,
        'can_edit': user and user in team.members,
        'post_to': '/team/%s/edit' % team.team_id,
        'page': 'team_profile',
    }

@get('/team/new')
@kajiki_view('team')
def team_profile_new():
    return {
        'is_new': True,
        'can_edit': True,
        'post_to': '/team/new',
        'page': 'new_team',
    }

@post('/team/new')
def team_profile_new():
    user = model.Session.get_identity(request)
    if not user:
        abort(403, 'You must be logged in to create a team')

    name = request.forms.get('name')
    website = request.forms.get('website')
    team_pic = request.files.get('profile_pic')

    if not validators.length(name, min=1):
        # TODO: Blow up
        pass

    if website and not website.startswith('http://') and not website.startswith('https://'):
        website = 'http://' + website

    if website and not validators.url(website):
        # TODO: blow up
        pass

    team = model.Team(name, website)
    team.members.append(user)

    if team_pic:
        if team_pic.filename and team_pic.file:
            # For some reason this isn't working, just use the dumb split
            #name, ext = os.path.splittext(profile_pic.filename)
            ext = team_pic.filename.split('.', 1)[-1]
            if ext not in ('png', 'jpg', 'jpeg', 'gif'):
                return 'File extension not allowed'

            pic_asset = model.Asset(team_pic.filename, ext[1:],
                                    helpers.util.save_asset(team_pic))
            team.profile_pic = pic_asset
            db.session.add(pic_asset)

    db.session.add(team)
    db.session.commit()

    redirect('/team/%s' % team.team_id)


@post('/team/<id>/edit')
def do_edit_team(id):
    pass

@route('/team/<id>/team_pic')
def profile_pic(id):
    team_pic = db.session.query(model.Asset)\
        .join(model.Team)\
        .filter_by(team_id=id).first()

    if team_pic is None:
        # If they haven't uploaded a profile pic yet, show the default one
        return static_file('default-team-pic.png', root='resources/images',
                           mimetype='image/png')

    # Find the file on disk and serve it up
    base_path = helpers.util.from_config_yaml('asset_save_location')
    return static_file(team_pic.filename, root=base_path,
                       mimetype='image/%s' % team_pic.type)