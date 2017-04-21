#! /usr/bin/env python3

"""
Security Check
"""

import functools

from bottle import abort

from showandtell.model import Session


def security_check(check_type, *dec_args, **dec_kwargs,):
    def decorator(secure_func):
        @functools.wraps(secure_func)
        def wrapper(*args, **kwargs):
            identity = Session.get_identity()
            if check_type == 'admin':
                if not identity or not identity.is_admin:
                    abort(403, 'You are not allowed to view the admin panel')
            elif check_type == 'logged_in':
                if not identity:
                    abort(403, 'You must be logged in to %s' %
                          dec_kwargs['action'])
            elif check_type == 'same_user':
                if not identity or identity.multipass_username != kwargs['username']:
                    abort(403, 'You are not allowed to edit users other than yourself')
            else:
                raise ValueError('Invalid check_type "%s" specified on the security_check decorator' % check_type)

            return secure_func(*args, **kwargs)

        return wrapper

    return decorator
