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

    print( "Number of assets:", len(project.assets) )
    if project.assets:
        for asset in project.assets:
            print( asset.assets.name )

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

    project_files = request.files.getall('project-files')        

    # Update all of the text entries for the project
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

    # Remove any selected files from the project
    num_assets = request.forms.get('num_assets')
    if num_assets:
        print( num_assets )
        for i in range(int(num_assets)):
            cur_asset = request.forms.get('asset-' + str(i))
            
            # Get the assets the user selected and delete them
            if cur_asset:
                # Convert the string into the asset id
                cur_asset = int(cur_asset.split()[-1])
                print("Asset to delete", cur_asset)
                
                asset = db.session.query(model.association_tables.ProjectAsset).filter_by(asset_id=cur_asset).one()
                project.assets.remove(asset)
            
    # Add any new files that were uploaded to the project
    if project_files:
        for i, file in enumerate(project_files):
            if file.filename and file.file:
                file_path = helpers.util.save_asset(file)

                # Debug
                print( file.filename )
                print( file.filename.split('.')[-1] )
                print( file.file )

                # Make the cross-reference between the new asset and the project
                xref = model.association_tables.ProjectAsset()
                xref.assets = model.Asset(file.filename, file.filename.split('.')[1], file_path)
                xref.role = "This is currently defunct"
                project.assets.append(xref)


                
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

    print( len(project.assets) )
    if project.assets:
        for asset in project.assets:
            print( asset.assets.name )

    return {
        'project': project,
        'can_edit': can_edit(user, project.team),
    }

''' Still in progress
@route('/projects/<id>/download')
def download_project(id):

    project = db.session.query(model.Project).filter_by(project_id=id).first()

    if len(project.assets) > 1:
        # TODO: Zip files and download all the assets
        print( "Oops!" )
    else:
        print("File name:", project.assets[0].assets.name)
        print("File path:", project.assets[0].assets.filename)
        return static_file( project.assets[0].assets.name, root=project.assets[0].assets.filename)
'''