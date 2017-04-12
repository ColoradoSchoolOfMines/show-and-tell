#! /usr/bin/env python3

"""
Admin Page
"""

from bottle import route, post, static_file, request, abort
from showandtell import helpers, kajiki_view, db
from showandtell.model import Project, Team, Session


@route('/admin')
@kajiki_view('admin_panel')
def admin_panel():
    identity = Session.get_identity(request)
    if not identity or not identity.is_admin:
        abort(403, 'You are not allowed to view the admin panel')

    t = Team('Mehtabyte')
    algobowl = Project(
        t, 'AlgoBowl', 'First place Spring 2017 AlgoBOWL project', 'shell_script')
    algobowl.status = 'verified'
    algobowl.project_id = 10

    dp = Project(t, 'Dynamic Programming', 'Cool project', 'shell_script')
    dp.project_id = 1

    sat = Project(t, 'Show and Tell', 'this', 'website',
                  website='https://showandtell.mines.edu')
    sat.status = 'rejected'
    sat.project_id = 8

    projects = [algobowl, dp, sat]

    sort_order = ['unverified', 'rejected', 'verified']
    projects = sorted(projects, key=lambda p: sort_order.index(p.status))

    return {
        'projects': projects,
        'page': 'admin',
    }


@route('/admin/<project_id>/verify')
def verify_project(project_id):
    identity = Session.get_identity(request)
    if not identity or not identity.is_admin:
        abort(403, 'You are not allowed to view the admin panel')

    project = Project.get_by_id(project_id)
    project.verify()

    redirect('/admin')


@post('/admin/<project_id>/reject')
def reject_project(project_id):
    identity = Session.get_identity(request)
    if not identity or not identity.is_admin:
        abort(403, 'You are not allowed to view the admin panel')

    reason = request.forms.get('reason')

    if not reason or len(reason.split()) == 0:
        abort(400, 'You need to enter a reason')

    project = Project.get_by_id(project_id)
    project.reject(reason)

    redirect('/admin')
