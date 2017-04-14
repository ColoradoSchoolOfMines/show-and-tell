#! /usr/bin/env python3

"""
Person Model
"""

from showandtell import helpers
from showandtell.db import Base
from showandtell.model.association_tables import person_team_xref

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref


class Person(Base, dict):

    def __init__(self, username):
        self.multipass_username = username
        self.name = helpers.mpapi.user_info(username)['gecos']

    def get_info_for_search(self):
        """ Get Info for Search. Don't return anything unnecssary """
        return {
            'user_id': self.user_id,
            'multipass_username': self.multipass_username,
            'name': self.name,
        }

    __tablename__ = 'people'

    # Fields
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    profile_pic_id = Column(Integer, ForeignKey('assets.asset_id'))
    multipass_username = Column(String, nullable=False)
    name = Column(String, nullable=False)
    bio = Column(String)
    github_username = Column(String)
    website = Column(String)
    is_admin = Column(Boolean, default=False)

    # Relationships
    profile_pic = relationship('Asset', back_populates='person')
    teams = relationship('Team', secondary=person_team_xref,
                         back_populates='members')
    sessions = relationship('Session', back_populates="user")
