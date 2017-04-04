#! /usr/bin/env python3

"""
Person Model
"""

from showandtell.db import DeclarativeBase, session
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Person(DeclarativeBase):
    __tablename__ = 't_people'

    # Fields
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    github_username = Column(String)
    website = Column(String)
