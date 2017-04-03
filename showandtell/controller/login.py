#! /usr/bin/env python3

""" Login Module """

from bottle import get, post
import kajiki


@get('/login')
def login():
    template = kajiki.XMLTemplate('<h1>Login</h1>')
    return template().render()


@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

@post('/logout')
def logout():
    pass

def check_login(username, password):
    return true
