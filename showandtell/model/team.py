#! /usr/bin/env python3

"""
Team Model
"""

from showandtell.db import DeclarativeBase, session
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Team:
    __tablename__ = 't_teams'

    # Fields
    team_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    website = Column(String)
