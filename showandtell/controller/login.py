#! /usr/bin/env python3

""" Login Controller """

from bottle import route, get, post, request, redirect
import requests
import urllib.parse

from showandtell import helpers, kajiki_view


@get('/login')
@kajiki_view('login')
def login():
    return {'page': 'login', 'login': None}


@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    # TODO: Exception handling
    if multipass_auth(username, password):
        # TODO: Create session
        redirect('/users/%s' % username)
    else:
        return "<p>Login failed.</p>"


@route('/logout')
def logout():
    # TODO: Acutally log out
    redirect('/')


def multipass_auth(username, password):
    """ Authenticate using MultiPass via Jack Rosenthal's Unofficial API """

    mpapi_base = helpers.util.from_config_yaml('mpapi_base')
    auth_request = requests.post(urllib.parse.urljoin(mpapi_base, 'auth'), data={
        'username': username,
        'password': password,
    })

    return auth_request.json()['result'] == 'success'
