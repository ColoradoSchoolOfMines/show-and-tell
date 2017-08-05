#! /usr/bin/env python3

"""
Asset Model
"""

from showandtell.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Asset(Base):

    def __init__(self, name, asset_type, filename, version_number=1, thumbnail=None):
        self.name = name
        self.type = asset_type
        self.filename = filename
        self.thumbnail = thumbnail
        self.version_number = version_number

    __tablename__ = 'assets'

    # Fields
    asset_id = Column(Integer, autoincrement=True, primary_key=True)
    version_number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    thumbnail = Column(String, nullable=True)

    team = relationship('Team', back_populates='profile_pic')
    person = relationship('Person', back_populates='profile_pic')
    project = relationship('ProjectAsset', back_populates='assets')
