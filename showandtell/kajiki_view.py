#! /usr/bin/env python3

"""
Defines the Kajiki View Decorator
"""

import functools
from kajiki import PackageLoader

loader = PackageLoader()

# Used code example from here:
# https://buxty.com/b/2013/12/jinja2-templates-and-bottle/
# but customized for kajiki instead
def kajiki_view(template_name):
    """ Defines the kajiki_view decorator """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            response = view_func(*args, **kwargs)

            if isinstance(response, dict):
                # If the decorated function returns a dictionary, throw that to
                # the template
                Template = loader.load('showandtell.template.%s' % template_name)
                t = Template(**response)
                return t.render()
            else:
                return response

        return wrapper

    return decorator
