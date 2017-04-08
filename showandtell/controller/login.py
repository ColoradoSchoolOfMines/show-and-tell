#! /usr/bin/env python3

"""
Login Controller
"""

from bottle import route, get, post, request, redirect
import requests
import urllib.parse

from showandtell import helpers, kajiki_view


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

    print(username, password)

    if username is None or password is None:
        redirect('/login?enter_credentials=true')

    # TODO: Exception handling
    if multipass_auth(username, password):
        # TODO: Create session
        redirect('/user/%s' % username)
    else:
        redirect('/login?bad_login=true')


@route('/logout')
def logout():
    # TODO: Acutally log out
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
