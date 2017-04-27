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

    # All the raw data from the form
    team_id = request.forms.get('team-id')
    name = request.forms.get('name')
    description = request.forms.get('description')
    project_type = request.forms.get('project-type')
    
    # Take the team id and get the team object
    team = db.session.query(model.Team).filter_by(team_id=team_id).one()

    # If the user didn't enter a website, 
    # set it to none so it's null
    website = request.forms.get('website')
    if website == '':
        website = None
    
    # Create a new row in the project table
    project = model.Project(team, name, description, project_type, website)

    db.session.add(project)
    db.session.commit()

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
    print("Hello world!")
