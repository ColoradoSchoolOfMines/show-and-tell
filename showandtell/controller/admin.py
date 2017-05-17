#! /usr/bin/env python3

"""
Admin Page
"""

from bottle import route, post, static_file, request, abort, redirect
from showandtell import helpers, kajiki_view, db, security_check, logged_in
from showandtell.model import Project, Team, Session


@route('/admin')
@kajiki_view('admin_panel')
@logged_in('view the admin panel')
@security_check('admin')
def admin_panel():
    projects = db.session.query(Project).all()

    # Sort the projects putting unverified before rejected before verified
    sort_order = ['unverified', 'rejected', 'verified']
    projects = sorted(projects, key=lambda p: sort_order.index(p.status))

    return {
        'projects': projects,
        'page': 'admin',
    }


@route('/admin/<project_id>/verify')
@logged_in('view the admin panel')
@security_check('admin')
def verify_project(project_id):
    project = Project.get_by_id(project_id)
    project.verify()

    redirect('/admin')


@post('/admin/<project_id>/reject')
@logged_in('view the admin panel')
@security_check('admin')
def reject_project(project_id):
    reason = request.forms.get('reason')

    if not reason or len(reason.split()) == 0:
        abort(400, 'You need to enter a reason')

    project = Project.get_by_id(project_id)
    project.reject(reason)

    redirect('/admin')
