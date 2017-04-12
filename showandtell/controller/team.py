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
    user = model.Session.get_identity(request)
    team_result = db.session.query(model.Team).filter_by(
        team_id=id)

    if not team_result.first():
        abort(404, 'No profile found for team #%s' % id)

    team = team_result.one()

    return {
        'team': team,
        'is_new': bool(request.GET.get('just_created')),
        'can_edit': user and user in team.members,
        'page': 'team_profile',
    }

@post('/team/new')
def team_profile_new():
    user = model.Session.get_identity(request)
    if not user:
        abort(403, 'You must be logged in to create a team')

    name = request.forms.get('name')

    if not validators.length(name, min=1):
        # TODO: Blow up
        pass

    team = model.Team(name, None)
    team.members.append(user)

    db.session.add(team)
    db.session.commit()

    redirect('/team/%s?just_created=true' % team.team_id)


@post('/team/<id>/edit')
def do_edit_team(id):
    user = model.Session.get_identity(request)
    team = db.session.query(model.Team)\
        .filter_by(team_id=id).one();

    if not user or user not in team.members:
        abort(403, 'You do not have permission to edit this team')


    name = request.forms.get('name')
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
            team.profile_pic = pic_asset
            db.session.add(pic_asset)

    if not validators.length(name, min=1):
        # TODO: Blow up
        pass

    if website and not website.startswith('http://') and not website.startswith('https://'):
        website = 'http://' + website

    if website and not validators.url(website):
        # TODO: blow up
        pass

    team.name = name
    team.website = website
    db.session.add(team)
    db.session.commit()

    redirect('/team/%s' % id)

@route('/team/<id>/team_pic')
def profile_pic(id):
    team_pic = db.session.query(model.Asset)\
        .join(model.Team)\
        .filter_by(team_id=id).first()

    print(team_pic)

    if team_pic is None:
        # If they haven't uploaded a profile pic yet, show the default one
        return static_file('default-team-pic.png', root='resources/images',
                           mimetype='image/png')

    # Find the file on disk and serve it up
    base_path = helpers.util.from_config_yaml('asset_save_location')
    return static_file(team_pic.filename, root=base_path,
                       mimetype='image/%s' % team_pic.type)