#! /usr/bin/env python3

"""
Search Controller
"""

from bottle import route, request, abort
from showandtell import db, kajiki_view, helpers, model
from showandtell.model import Person, Team, Project


@route('/search')
@kajiki_view('searchresults')
def search():
    query = request.GET.get('q')
    search_type = request.GET.get('type')
    if search_type not in ('all', 'people', 'teams', 'projects'):
        abort('Search type must either "all", "people", "teams" or "projects"')

    results = {
        'page': 'searchresults',
        'query': query,
        'search_type': search_type,
    }

    if search_type == 'all':
        results['people'] = find_users(query)
        results['teams'] = find_teams(query)
        results['projects'] = find_projects(query)
    elif search_type == 'people':
        results['people'] = find_users(query)
    elif search_type == 'teams':
        results['teams'] = find_teams(query)
    elif search_type == 'projects':
        results['projects'] = find_projects(query)

    return results


@route('/search/<entity>')
def search_users(entity):
    query = request.GET.get('q')

    if entity not in ('users', 'teams', 'projects'):
        abort('Cannot search for %s' % entity)
    elif entity == 'users':
        return {'people': find_users(query)}
    elif entity == 'teams':
        return {'teams': find_teams(query)}
    elif entity == 'projects':
        return {'projects': find_projects(query)}


def find_users(query):
    people = db.session.query(Person)\
        .filter(Person.multipass_username.ilike('%%%s%%' % query) |
                Person.name.ilike('%%%s%%' % query) |
                Person.github_username.ilike('%%%s%%' % query) |
                Person.bio.ilike('%%%s%%' % query) |
                Person.website.ilike('%%%s%%' % query))\
        .all()
    return [p.info_dict() for p in people]


def find_teams(query):
    teams = db.session.query(Team)\
        .filter(Team.name.ilike('%%%s%%' % query) |
                Team.website.ilike('%%%s%%' % query))\
        .all()

    return [t.info_dict() for t in teams]


def find_projects(query):
    projects = db.session.query(Project)\
        .filter(Project.name.ilike('%%%s%%' % query) |
                Project.website.ilike('%%%s%%' % query) |
                Project.description.ilike('%%%s%%' % query))\
        .all()

    return [p.info_dict() for p in projects]
