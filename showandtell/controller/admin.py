#! /usr/bin/env python3

"""
Admin Page
"""

from bottle import route, static_file, request, abort
from showandtell import helpers, kajiki_view, db
from showandtell.model import *


@route('/admin')
@kajiki_view('admin_panel')
def admin_panel():
    identity = Session.get_identity(request)
    if not identity or not identity.is_admin:
        abort(403, 'You are not allowed to view the admin panel')

    t = Team('Mehtabyte')
    algobowl = Project(t, 'AlgoBowl', 'Cool project', 'shell_script')
    dp = Project(t, 'Dynamic Programming', 'Cool project', 'shell_script')

    return {
        'unverified_projects': [algobowl, dp],
        'verified_projects': [],
        'rejected_projects': [],
        'page': 'admin',
    }

@post('/admin/verify/<project_id>')
def verify_project(project_id):

