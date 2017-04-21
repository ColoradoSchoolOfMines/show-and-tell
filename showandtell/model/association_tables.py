#! /usr/bin/env python3

"""
Cross Reference Tables
"""

from showandtell.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

person_team_xref = Table('person_team_xref', Base.metadata,
                         Column('person_id', Integer,
                                ForeignKey('people.user_id')),
                         Column('team_id', Integer,
                                ForeignKey('teams.team_id')))


class ProjectAsset(Base):
    """
    Project to Asset Cross Reference Table

    I am having to make this its own class because we have metadata on the
    relationship
    """

    __tablename__ = 'project_asset_xref'

    # Fields
    project_id = Column(Integer, ForeignKey('projects.project_id'),
                        primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.asset_id'),
                      primary_key=False)
    role = Column(String, nullable=False)

    # Relationships
    project = relationship('Project', back_populates='assets')
    assets = relationship('Asset', back_populates='project')
