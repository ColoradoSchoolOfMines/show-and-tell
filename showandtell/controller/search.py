#! /usr/bin/env python3

"""
Search Controller
"""

from bottle import route, request
from showandtell import db, kajiki_view, helpers, model
from showandtell.model import Person, Team


@route('/search')
def search():
    query = request.GET.get('q')
    return {
        'people': find_users(query),
        'teams': find_teams(query),
    }


@route('/search/users')
def search_users():
    query = request.GET.get('q')
    return {'people': find_users(query)}


@route('/search/teams')
def search_teams():
    query = request.GET.get('q')
    return {'teams': find_teams(query)}


def find_users(query):
    people = db.session.query(Person)\
        .filter((Person.multipass_username.ilike('%%%s%%' % query)) |
                (Person.name.ilike('%%%s%%' % query)))\
        .all()
    return [p.info_dict() for p in people]


def find_teams(query):
    teams = db.session.query(Team).filter_by(name=query).all()
    return [t.info_dict() for t in teams]
