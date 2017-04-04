#! /usr/bin/env python3

"""
Asset Model
"""

from showandtell.db import DeclarativeBase, session
from sqlalchemy import Column, Integer, String, Binary, ForeignKey
from sqlalchemy.orm import relationship


class Asset:
    __tablename__ = 't_assets'

    # Fields
    asset_id = Column(Integer, autoincrement=True, primary_key=True)

    # TODO: we need to have one and only one of these
    project_id = Column(Integer, ForeignKey('t_projects.project_id'))
    team_id = Column(Integer, ForeignKey('t_teams.team_id'))
    person_id = Column(Integer, ForeignKey('t_people.user_id'))

    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    data = Column(Binary, nullable=False)
