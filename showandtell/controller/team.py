#! /usr/bin/env python3

"""
Team Controller
"""

from bottle import route, get, post, request, redirect, static_file, abort
from showandtell import db, kajiki_view, helpers, model, security_check, logged_in
import validators
import os


def can_edit(ident, team):
    if ident == None:
        return False

    admin_edit = ident.is_admin and helpers.util.from_config_yaml('admin_edit')
    return (ident and ident in team.members) or admin_edit


def query_team(id, edit=False):
    user = model.Session.get_identity()
    team = db.session.query(model.Team).filter_by(team_id=id).first()

    if edit and not can_edit(user, team):
        abort(403, 'You do not have permission to edit this team')

    return (team, user)


@route('/team/<id>')
@kajiki_view('team')
def team_profile(id):
    (team, user) = query_team(id)

    if not team:
        abort(404, 'No profile found for team #%s' % id)

    return {
        'team': team,
        'is_new': bool(request.GET.get('just_created')),
        'can_edit': can_edit(user, team),
        'page': 'team_profile',
    }


@post('/team/new')
@logged_in('create a team')
def team_profile_new():
    user = model.Session.get_identity()
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
@logged_in('edit a team')
def do_edit_team(id):
    (team, user) = query_team(id, edit=True)

    name = request.forms.get('name')
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


def add_member(uid, team):
    person = db.session.query(model.Person).filter_by(user_id=uid).one()
    if person:
        if person not in team.members:
            team.members.append(person)
        else:
            abort(400, 'Person #%s is already a member of team' % uid)
    else:
        abort(400, 'Person #%s does not exist' % uid)


def remove_member(uid, team):
    person = db.session.query(model.Person).filter_by(user_id=uid).one()
    if person:
        if person in team.members:
            team.members.remove(person)
        else:
            abort(400, 'Person #%s is not a member of team' % uid)
    else:
        abort(400, 'Person #%s does not exist' % uid)


@logged_in('edit a team')
@post('/team/<id>/members')
def mod_members(id):
    (team, user) = query_team(id, edit=True)

    add = []
    remove = []

    if not request.query.type or request.query.type == 'json':
        add = [p.get('user_id') for p in request.json.get('add') or []]
        remove = [p.get('user_id') for p in request.json.get('remove') or []]

    elif request.query.type == 'form':
        form_add = request.forms.get('add')
        form_remove = request.forms.get('remove')
        if form_add:
            add.append(request.forms.get('add'))

        elif form_remove:
            remove.append(request.forms.get('remove'))

    else:
        abort(400, 'Member modification not form or json')

    for p in add:
        add_member(p, team)

    for p in remove:
        remove_member(p, team)

    db.session.add(team)
    db.session.commit()

    redirect('/team/%s' % id)


@get('/team/<id>/members')
def get_members(id):
    (team, user) = query_team(id)
    return {'members': [p.info_dict() for p in team.members]}


def get_pic(id, thumb=False):
    """ Returns the actual profile picture """
    profile_pic = db.session.query(model.Asset)\
        .join(model.Team)\
        .filter_by(team_id=id).first()

    if profile_pic is None:
        # If they haven't uploaded a profile pic yet, show the default one
        return static_file('default-team-pic.png', root='resources/images',
                           mimetype='image/png')

    # Find the file on disk and serve it up
    base_path = helpers.util.from_config_yaml('asset_save_location')
    return static_file(profile_pic.thumbnail if thumb and profile_pic.thumbnail
                       else profile_pic.filename,
                       root=base_path, mimetype='image/png')


@route('/team/<id>/profile_pic.png')
def profile_pic(id):
    return get_pic(id)


@route('/team/<id>/profile_thumb.png')
def profile_thumb(id):
    return get_pic(id, thumb=True)
