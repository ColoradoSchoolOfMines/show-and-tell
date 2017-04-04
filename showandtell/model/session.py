#! /usr/bin/env python3

"""
Session Model
"""

from showandtell.db import DeclarativeBase, session
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Session:
    __tablename__ = 't_sessions'

    # Fields
    session_id = Column(Integer, autoincrement=True, primary_key=True)
    expires_on = Column(DateTime, autoincrement=True, primary_key=True)
    session_cookie = Column(String, nullable=False) # Cookie for the Session
    user_id = Column(Integer, ForeignKey('t_people.user_id'))

    # Relationships
    user = relationship('Person')
