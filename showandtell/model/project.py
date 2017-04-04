#! /usr/bin/env python3

"""
Project Model
"""

from showandtell.db import DeclarativeBase
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Project(DeclarativeBase):
    __tablename__ = 't_projects'

    # Fields
    project_id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    name = Column(String, unique=True, nullable=False)
    website = Column(String)

    # Relationships
    assets = relationship('Asset')
