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
        'page': 'submit_project'
    }

# Get the contents submitted from submit a project
@post('/submit/new')
def submit_project():
    user = model.Session.get_identity()

    name = request.forms.get('name')

    website = request.forms.get('website')

    print('name')
    print('webiste')


