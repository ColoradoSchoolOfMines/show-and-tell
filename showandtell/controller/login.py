#! /usr/bin/env python3

""" Login Controller """

from bottle import route, get, post, request, redirect
import kajiki
import requests
import urllib.parse

import showandtell


@get('/login')
def login():
    # TODO: Make this templated
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''


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
    pass


def multipass_auth(username, password):
    """ Authenticate using MultiPass via Jack Rosenthal's Unofficial API """

    mpapi_base = showandtell.helpers.util.from_config_yaml('mpapi_base')
    auth_request = requests.post(urllib.parse.urljoin(mpapi_base, 'auth'), data={
        'username': username,
        'password': password,
    })

    return auth_request.json()['result'] == 'success'
