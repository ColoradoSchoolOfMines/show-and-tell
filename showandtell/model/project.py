#! /usr/bin/env python3

"""
Project Model
"""

from showandtell.db import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Project(DeclarativeBase):
    __tablename__ = 'projects'

    # Fields
    project_id = Column(Integer, autoincrement=True, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.team_id'), nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    name = Column(String, unique=True, nullable=False)
    website = Column(String)

    # Relationships
    assets = relationship('ProjectAsset')
    team = relationship('Team', back_populates='projects')
