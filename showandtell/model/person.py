#! /usr/bin/env python3

"""
Person Model
"""

from showandtell.db import DeclarativeBase
from showandtell.model.association_tables import person_team_xref

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

class Person(DeclarativeBase):
    __tablename__ = 'people'

    # Fields
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    profile_pic_id = Column(Integer, ForeignKey('assets.asset_id'))
    name = Column(String, nullable=False)
    github_username = Column(String)
    website = Column(String)

    # Relationships
    profile_pic = relationship('Assset',
                               backref=backref('people', use_list=False))
    teams = relationship('Team', secondary=person_team_xref,
                         back_populates='people')
