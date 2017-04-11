#! /usr/bin/env python3

"""
MultiPass API Wrapper
"""
import urllib.parse
import requests
from showandtell.helpers import util


def _api_url(path):
    return urllib.parse.urljoin(util.from_config_yaml('mpapi_base'), path)


def auth(username, password):
    """ Authenticate using MultiPass via Jack Rosenthal's Unofficial API """

    auth_request = requests.post(_api_url('auth'), data={
        'username': username,
        'password': password,
    })

    # TODO: Logging

    if not auth_request.ok:
        return False

    return auth_request.json()['result'] == 'success'


def user_info(username):
    user_info_request = requests.get(_api_url('uid/%s' % username))

    if not user_info_request.ok or user_info_request.json()['result'] != 'success':
        return None

    return user_info_request.json()['attributes']
