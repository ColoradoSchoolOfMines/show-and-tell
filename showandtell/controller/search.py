#! /usr/bin/env python3

"""
Search Controller
"""

from bottle import route
from showandtell import db, kajiki_view, helpers, model
from showandtell.model import Person, Team


@route('/search/<query>')
def search(query):
    pass


@route('/search/users/<query>')
def search_users(query):
    people = db.session.query(Person)\
        .filter((Person.multipass_username.ilike('%%%s%%' % query)) |
                (Person.name.ilike('%%%s%%' % query)))\
        .all()

    return {'people': [p.info_dict() for p in people]}


@route('/search/teams/<query>')
def search_teams(query):
    teams = db.session.query(Team).filter_by(name=query).all()
    return {'teams': [t.info_dict() for t in teams]}
