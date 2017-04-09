#! /usr/bin/env python3

"""
Session Model
"""

from showandtell import model
from showandtell.db import Base, session
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

import datetime


class Session(Base):

    def __init__(self, username, session_token):
        self.user_id = session.query(model.Person)\
            .filter_by(multipass_username=username)\
            .first()\
            .user_id

        self.expires_on = datetime.datetime.now()
        self.session_cookie = session_token

    __tablename__ = 'sessions'

    # Fields
    session_id = Column(Integer, autoincrement=True, primary_key=True)
    expires_on = Column(DateTime, nullable=False)
    session_cookie = Column(String, nullable=False)  # Cookie for the Session
    user_id = Column(Integer, ForeignKey('people.user_id'), nullable=False)

    # Relationships
    user = relationship('Person', back_populates='sessions')
