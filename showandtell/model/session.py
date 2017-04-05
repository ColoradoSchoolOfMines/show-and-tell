#! /usr/bin/env python3

"""
Session Model
"""

from showandtell.db import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Session(DeclarativeBase):
    __tablename__ = 'sessions'

    # Fields
    session_id = Column(Integer, autoincrement=True, primary_key=True)
    expires_on = Column(DateTime, autoincrement=True, primary_key=True)
    session_cookie = Column(String, nullable=False)  # Cookie for the Session
    user_id = Column(Integer, ForeignKey('people.user_id'), nullable=False)

    # Relationships
    user = relationship('Person')
