#! /usr/bin/env python3

"""
Utility Functions
"""

from datetime import date
import yaml

from showandtell import helpers

def get_copyright_string(start_year):
    end_year = date.today().year
    if end_year > start_year:
        return '&copy; %d-%d Mines ACM. All Rights Reserved.' % (start_year, end_year)
    else:
        return '&copy; %d Mines ACM. All Rights Reserved.' % start_year

def from_config_yaml(key, force_reload=False):
    if helpers.config_yaml is None or force_reload:
        with open('config.yaml') as config:
            helpers.config_yaml = yaml.load(config)

    return helpers.config_yaml[key]
