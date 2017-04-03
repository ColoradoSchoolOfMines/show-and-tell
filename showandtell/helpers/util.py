#! /usr/bin/env python3

"""
Utility Functions
"""

from datetime import date

def get_copyright_string(start_year):
    end_year = date.today().year
    if end_year > start_year:
        return '&copy; %d-%d Mines ACM. All Rights Reserved.' % (start_year, end_year)
    else:
        return '&copy; %d Mines ACM. All Rights Reserved.' % start_year

def get_template_text(template_name):
    template = open('showandtell/template/%s.xhtml' % template_name)
    return str(template.read())
