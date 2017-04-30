#! /usr/bin/env python3

"""
Utility Functions
"""

import os
from datetime import date

import uuid

import yaml
from markupsafe import Markup

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

    if key in helpers.config_yaml:
        return helpers.config_yaml[key]

    return None


def app_name():
    return from_config_yaml('app_name')


def extra_template_context(identity):
    context = {
        'util': helpers.util,
        'identity': identity,
    }
    return context


def glyphicon(icon_name, *args, **kwargs):
    return Markup('<i class="glyphicon glyphicon-%s %s" %s></i>' % (
        icon_name,
        ' '.join(args),
        ' '.join('%s="%s"' % (k, v) for k, v in kwargs.items())
    ))


def faicon(icon_name, *args, **kwargs):
    return Markup('<i class="fa fa-%s %s" %s></i>' % (
        icon_name,
        ' '.join(args),
        ' '.join('%s="%s"' % (k, v) for k, v in kwargs.items())
    ))


def make_path():
    base_path = from_config_yaml('asset_save_location')
    real_filename = str(uuid.uuid4())
    return (os.path.join(base_path, real_filename), real_filename)


def get_asset_folder():
    base_path = from_config_yaml('asset_save_location')
    return base_path


def save_asset(uploaded_file):
    (full_path, filename) = make_path()
    uploaded_file.save(full_path)
    return filename


def delete_asset(file_name):
    base_path = from_config_yaml('asset_save_location')
    file_path = os.path.join(base_path, file_name)
    os.remove(file_path)

from PIL import Image


def upload_profile_pic(uploaded_file):
    if uploaded_file.content_length > 20000000:
        raise IOError('Content is too large')
    img = Image.open(uploaded_file.file)

    (w, h) = img.size
    s = min(w, h)
    tb = (h - s) / 2
    lr = (w - s) / 2
    img = img.crop((lr, tb, w - lr, h - tb))

    imgpath = make_path()
    img.resize((300, 300)).save(imgpath[0], format='png')
    thumbpath = make_path()
    img.thumbnail((64, 64))
    img.save(thumbpath[0], format='png')

    return (imgpath[1], thumbpath[1])
