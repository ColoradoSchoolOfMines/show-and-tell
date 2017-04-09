#! /usr/bin/env python3

"""
Utility Functions
"""

from datetime import date
from markupsafe import Markup
import yaml

from showandtell import helpers


def copyright_holder():
    return 'Jonathan Sumner Evans, Daichi Jameson, and Sam Sartor'


def copyright_year(start_year):
    end_year = date.today().year
    if end_year > start_year:
        return '%d-%d' % (start_year, end_year)
    else:
        return str(start_year)


def from_config_yaml(key, force_reload=False):
    if helpers.config_yaml is None or force_reload:
        with open('config.yaml') as config:
            helpers.config_yaml = yaml.load(config)

    return helpers.config_yaml[key]


def app_name():
    return from_config_yaml('app_name')


def extra_template_context(identity):
    context = {
        'util': helpers.util,
        'identity': identity,
    }
    return context


def glyphicon(icon_name):
    return Markup('<i class="glyphicon glyphicon-%s"></i>' % icon_name)


def faicon(icon_name):
    return Markup('<span class="fa fa-%s"></span>' % icon_name)
