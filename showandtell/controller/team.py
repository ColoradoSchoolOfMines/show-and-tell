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

def query_team(id, edit=True):
    user = model.Session.get_identity(request)
    team = db.session.query(model.Team)\
        .filter_by(team_id=id).one();

    if edit and (not user or user not in team.members):
        abort(403, 'You do not have permission to edit this team')

    return (team, user)

@post('/team/<id>/edit')
def do_edit_team(id):
    (team, user) = query_team(id)

    name = request.forms.get('name')
    website = request.forms.get('website')
    profile_pic = request.files.get('profile_pic')

    if profile_pic:
        if profile_pic.filename and profile_pic.file:
            try:
                (pic, thumb) = helpers.util.upload_profile_pic(profile_pic)
            except IOError as err:
                return "{}".format(err)
            asset = model.Asset(profile_pic.filename, "png", pic, thumbnail = thumb)
            team.profile_pic = asset
            db.session.add(asset)

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

@post('/team/<id>/members')
def mod_members(id):
    (team, user) = query_team(id)

    add = request.json.get('add') or []
    for p in add:
        uid = p.get('id')
        person = db.session.query(model.Person).filter_by(user_id=uid).first()
        if person: 
            if person not in team.members: team.members.append(person)
            else: abort(400, 'Person #%s is already a member of team' % uid)
        else: abort(400, 'Person #%s does not exist' % uid)

    remove = request.json.get('remove') or []
    for p in remove:
        uid = p.get('id')
        person = db.session.query(model.Person).filter_by(user_id=uid).first()
        if person: 
            if person in team.members: team.members.remove(person)
            else: abort(400, 'Person #%s is not a member of team' % uid)
        else: abort(400, 'Person #%s does not exist' % uid)

    db.session.commit()

@get('/team/<id>/members')
def get_members(id):
    (team, user) = query_team(id)

    out = []
    for p in team.members:
        out.append(p.info_dict())

    return {'members': out}

def get_pic(id, thumb = False):
    profile_pic = db.session.query(model.Asset)\
        .join(model.Team)\
        .filter_by(team_id=id).first()

    if profile_pic is None:
        # If they haven't uploaded a profile pic yet, show the default one
        return static_file('default-team-pic.png', root='resources/images',
                           mimetype='image/png')

    # Find the file on disk and serve it up
    base_path = helpers.util.from_config_yaml('asset_save_location')
    return static_file(profile_pic.thumbnail if thumb and profile_pic.thumbnail else profile_pic.filename,
                       root=base_path, mimetype='image/png')


@route('/team/<id>/profile_pic.png')
def profile_pic(id):
    return get_pic(id)

@route('/team/<id>/profile_thumb.png')
def profile_thumb(id):
    return get_pic(id, thumb = True)
