#! /usr/bin/env python3

"""
Cross Reference Tables
"""

from showandtell.db import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

person_team_xref = Table('person_team_xref', DeclarativeBase.metadata,
                         Column('person_id', Integer,
                                ForeignKey('people.user_id')),
                         Column('team_id', Integer,
                                ForeignKey('teams.team_id')))


class ProjectAsset(DeclarativeBase):
    """
    Project to Asset Cross Reference Table

    I am having to make this its own class because we have metadata on the
    relationship
    """

    __tablename__ = 'project_asset_xref'

    # Fields
    project_asset_id = Column(Integer, autoincrement=True, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.project_id'),
                        nullable=False)
    asset_id = Column(Integer, ForeignKey('assets.asset_id'), nullable=False)
    role = Column(String, nullable=False)

    # Relationships
    assets = relationship('Asset')
