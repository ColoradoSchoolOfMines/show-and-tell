#! /usr/bin/env python3

"""
Admin Page
"""

from bottle import route, post, static_file, request, abort
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
    algobowl.status = 'verified'
    dp = Project(t, 'Dynamic Programming', 'Cool project', 'shell_script')
    sat = Project(t, 'Show and Tell', 'this', 'website')
    sat.status = 'rejected'

    return {
        'projects': [algobowl, dp, sat],
        'page': 'admin',
    }


@post('/admin/verify/<project_id>')
def verify_project(project_id):
    identity = Session.get_identity(request)
    if not identity or not identity.is_admin:
        abort(403, 'You are not allowed to view the admin panel')
