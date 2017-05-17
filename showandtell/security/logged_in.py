#! /usr/bin/env python3

"""
Logged In
"""

import functools

from bottle import abort

from showandtell.model import Session


def logged_in(action):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            identity = Session.get_identity()
            if not identity:
                abort(403, 'You must be logged in to %s' % action)

            return f(*args, **kwargs)

        return wrapper

    return decorator
