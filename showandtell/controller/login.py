#! /usr/bin/env python3

"""
Login Controller
"""

from bottle import route, get, post, request, redirect, response
import requests
import urllib.parse
import uuid

from showandtell import helpers, kajiki_view, db
from showandtell.model import Session


@get('/login')
@kajiki_view('login')
def login():
    flash = {}
    if bool(request.GET.get('bad_login')):
        flash['content'] = 'Invalid MultiPass Credentials'
        flash['cls'] = 'error'

    if bool(request.GET.get('enter_credentials')):
        flash['content'] = 'Please enter your login credentials'
        flash['cls'] = 'error'

    return {'page': 'login', 'username': None, 'flash': flash}


@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    if username is None or password is None:
        redirect('/login?enter_credentials=true')

    if multipass_auth(username, password):
        session_token = uuid.uuid4()

        # Create the actual session
        user_session = Session(username, session_token)
        db.session.add(user_session)
        db.session.commit()

        response.set_cookie('session_token', str(session_token))

        redirect('/user/%s' % username)
    else:
        redirect('/login?bad_login=true')


@route('/logout')
def logout():
    session = db.session.query(showandtell.model.Session)\
        .filter_by(session_cookie=request.get_cookie('session_token')).delete()
    redirect('/')


def multipass_auth(username, password):
    """ Authenticate using MultiPass via Jack Rosenthal's Unofficial API """

    api_base = helpers.util.from_config_yaml('mpapi_base')
    auth_request = requests.post(urllib.parse.urljoin(api_base, 'auth'), data={
        'username': username,
        'password': password,
    })

    # TODO: Logging

    if not auth_request.ok:
        return False

    return auth_request.json()['result'] == 'success'
