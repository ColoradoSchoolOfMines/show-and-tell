#! /usr/bin/env python3

"""
Sumbit Project Controller
"""

from bottle import route, get, post, request, redirect, static_file, abort, response
from showandtell import db, kajiki_view, helpers, model, security_check, logged_in
import validators
import os
import uuid


def can_edit(ident, team):
    if ident is None:
        return False

    admin_edit = ident.is_admin and helpers.util.from_config_yaml('admin_edit')
    return (ident and ident in team.members) or admin_edit

# Go to the submit a project page


@route('/projects/<id>/edit')
@route('/submit')
@kajiki_view('edit_project')
@logged_in('modify a project')
def new_project(id=None):
    user = model.Session.get_identity()

    # This is slated to be removed for a more complex redirect
    if user == None:
        redirect('/login')

    if id == None:
        project = model.Project(None, None, None, None)
    else:
        project = db.session.query(
            model.Project).filter_by(project_id=id).one()

        if user not in project.team.members:
            abort(403, 'You are not on the team making this project!')

    return {
        'project': project,
        'teams': user.teams,
        # This is a placeholder for the moment,
        # I dunno what we're actually doing
        'types': ['Image', 'Video', 'Shell Script'],
        'page': 'submit_project',
    }

    # Get the contents submitted from submit a project


@post('/submit/new')
@logged_in('submit a new project')
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
        project = db.session.query(model.Project).filter_by(
            project_id=project_id).one()
        project.team = team
        project.name = name
        project.description = description
        project.type = project_type
        project.website = website
        project.status = 'unverified'

    project.repository = repository

    # Remove any un-selected files from the project
    asset_num = 0
    while True:
        cur_asset = request.forms.get('asset-' + str(asset_num))
        if cur_asset is None:
            break
        if request.forms.get('include-' + str(asset_num)) is None:
            # Convert the string into the asset id
            cur_asset = int(cur_asset)

            asset = db.session.query(model.association_tables.ProjectAsset).\
                filter_by(asset_id=cur_asset).one()
            helpers.util.delete_asset(asset.assets.filename)
            project.assets.remove(asset)
        asset_num += 1

    # Add any new files that were uploaded to the project
    if project_files:
        for i, file in enumerate(project_files):
            if file.filename and file.file:
                file_path = helpers.util.save_asset(file)

                # Make the cross-reference between the new asset and the
                # project
                xref = model.association_tables.ProjectAsset()
                xref.assets = model.Asset(
                    file.filename, file.filename.split('.')[1], file_path)
                xref.role = " "
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

    return {
        'project': project,
        'can_edit': can_edit(user, project.team),
    }

    from zipfile import ZipFile
from io import BytesIO


@get('/projects/<id>/download')
@security_check('admin')
@logged_in('downlaod project assets')
def download_project(id):

    project = db.session.query(model.Project).filter_by(project_id=id).first()
    root_path = helpers.util.get_asset_folder()

    if not project.assets:
        return None
    if len(project.assets) == 1:
        asset = project.assets[0].assets
        return static_file(asset.filename, root=root_path, download=asset.name)
    # Yes, this is very ugly
    # I'm very sorry
    else:
        download_name = '-'.join(project.name.split()) + '.zip'
        archive_name = str(uuid.uuid4())
        archive_path = os.path.join(root_path, archive_name)

        archive = ZipFile(archive_path, mode='x')

        # Stick all of the assets into the zip
        for project_asset in project.assets:
            asset = project_asset.assets
            asset_path = os.path.join(root_path, asset.filename)
            archive.write(asset_path, asset.name)

        archive.close()

        # This is a stupid solution,
        # but makes it so no zip file is left on disk after the assets are
        # downloaded
        zip_contents = open(archive_path, 'rb')
        archive_file = BytesIO(zip_contents.read())
        zip_contents.close()
        os.remove(archive_path)

        response.headers['Content-Type'] = 'application/zip'
        response.headers[
            "Content-Disposition"] = "attachment; filename={}".format(download_name)
        return archive_file
        # return static_file(archive_name, root=root_path,
        # download=download_name)
