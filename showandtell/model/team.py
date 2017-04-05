#! /usr/bin/env python3

"""
Team Model
"""

from showandtell.db import DeclarativeBase
from showandtell.model.association_tables import person_team_xref

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref


class Team(DeclarativeBase):
    __tablename__ = 'teams'

    # Fields
    team_id = Column(Integer, autoincrement=True, primary_key=True)
    profile_pic_id = Column(Integer, ForeignKey('assets.asset_id'))
    name = Column(String, nullable=False)
    website = Column(String)

    # Relationships
    profile_pic = relationship('Asset',
                               backref=backref('people', use_list=False))
    members = relationship('Person', secondary=person_team_xref,
                           back_populates='teams')
    projects = relationship('Project', back_populates='teams')
