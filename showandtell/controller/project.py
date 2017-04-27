#! /usr/bin/env python3

"""
Sumbit Project Controller
"""

from bottle import route, get, post, request, redirect, static_file, abort
from showandtell import db, kajiki_view, helpers, model, security_check
import validators
import os

# Go to the submit a project page
@route('/submit')
@kajiki_view('edit_project')
def new_project():
    
    user = model.Session.get_identity()

    if user == None:
        redirect('/login')

    print("The cake is a lie!")
    return {
        # Yes, this is a hack to get the text area to work properly
        'empty': '',
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
    
    # Create a new row in the project table
    project = model.Project(team, name, description, project_type, website)
    project.repository = repository

    db.session.add(project)
    db.session.commit()

    redirect('/projects/' + str(project.project_id))

    ''' Hooray for debugging
    print("Team",team)
    print("name",name)
    print("description",description)
    print("project_type",project_type)
    print("website",website)
    '''

@route('/projects/<id>')
@kajiki_view('view_project')
def view_project(id):
    
    project = db.session.query(model.Project).filter_by(project_id=id).first()

    if not project:
        abort(404, 'Project not found!')

    return {
        'project': project,
    }