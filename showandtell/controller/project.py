#! /usr/bin/env python3

"""
Sumbit Project Controller
"""

from bottle import route, get, post, request, redirect, static_file, abort
from showandtell import db, kajiki_view, helpers, model, security_check
import validators
import os

def can_edit(ident, team):
    admin_edit = ident.is_admin and helpers.util.from_config_yaml('admin_edit')
    return (ident and ident in team.members) or admin_edit

# Go to the submit a project page
@route('/projects/<id>/edit')
@route('/submit')
@kajiki_view('edit_project')
def new_project(id=None):
    
    user = model.Session.get_identity()

    # This is slated to be removed for a more complex redirect
    if user == None:
        redirect('/login')

    if id == None:
        project = model.Project(None, None, None, None)
    else:
        project = db.session.query(model.Project).filter_by(project_id=id).one()

    return {
        # Yes, this is a hack to get the text area to work properly
        'empty': '',
        'project': project,
        'teams': user.teams,
        # This is a placeholder for the moment, 
        # I dunno what we're actually doing
        'types': ['Image', 'Video', 'Shell Script'],
        'page': 'submit_project',
    }

# Get the contents submitted from submit a project
@post('/submit/new')
def submit_project():
    user = model.Session.get_identity()

    project_id = request.forms.get('project_id')
    team_id = request.forms.get('team-id')
    # Take the team id and get the team object
    team = db.session.query(model.Team).filter_by(team_id=team_id).one()

    name = request.forms.get('name')
    description = request.forms.get('description')
    project_type = request.forms.get('project-type')
     
    # If the user didn't enter a website, 
    # set it to none so it's null
    website = request.forms.get('website')
    if website == '':
        website = None

    repository = request.forms.get('repository')
    if repository == '':
        repository = None

    project_pic = request.files.get('project_pic')
    if project_pic:
        print( project_pic )

    if not project_id:
        # Create a new row in the project table
        project = model.Project(team, name, description, project_type, website)
    else:
        project = db.session.query(model.Project).filter_by(project_id=project_id).one()
        project.team = team
        project.name = name
        project.description = description
        project.type = project_type
        project.website = website
        project.status = 'unverified'
   
    project.repository = repository

    db.session.add(project)
    db.session.commit()
    
    redirect('/projects/' + str(project.project_id))

@route('/projects/<id>')
@kajiki_view('view_project')
def view_project(id):
    
    user = model.Session.get_identity()
    project = db.session.query(model.Project).filter_by(project_id=id).first()

    if not project:
        abort(404, 'Project not found!')

    return {
        'project': project,
        'can_edit': can_edit(user, project.team),
    }