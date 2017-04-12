#! /usr/bin/env python3

"""
Project Model
"""

from showandtell.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Project(Base):

    def __init__(self, team, name, description, type, website=None):
        self.team = team
        self.name = name
        self.description = description
        self.type = type
        self.website = website

    __tablename__ = 'projects'

    # Fields
    project_id = Column(Integer, autoincrement=True, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.team_id'), nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    name = Column(String, unique=True, nullable=False)
    website = Column(String)
    verified = Column(Boolean)

    # Relationships
    assets = relationship('ProjectAsset', back_populates='project')
    team = relationship('Team', back_populates='projects')
