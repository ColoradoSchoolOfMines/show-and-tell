#! /usr/bin/env python3

"""
Session Model
"""

import datetime
from datetime import timedelta

from showandtell import model
from showandtell.db import Base, session
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Session(Base):

    def __init__(self, username, session_token):
        person = session.query(model.Person)\
            .filter_by(multipass_username=username)\
            .first()

        # TODO: should we be automatically creating user accounts?
        if not person:
            person = model.Person(username)
            session.add(person)
            session.commit()

        self.user_id = person.user_id
        self.session_cookie = session_token

        # Expire Token in a Month
        self.expires_on = datetime.datetime.now() + timedelta(days=30)

    @staticmethod
    def get_identity(request):
        user_session = session.query(Session)\
            .filter_by(session_cookie=request.get_cookie('session_token'))\
            .first()

        return None if user_session is None else user_session.user

    __tablename__ = 'sessions'

    # Fields
    session_id = Column(Integer, autoincrement=True, primary_key=True)
    expires_on = Column(DateTime, nullable=False)
    session_cookie = Column(String, nullable=False)  # Cookie for the Session
    user_id = Column(Integer, ForeignKey('people.user_id'), nullable=False)

    # Relationships
    user = relationship('Person', back_populates='sessions')
