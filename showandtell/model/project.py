#! /usr/bin/env python3

"""
Project Model
"""

from showandtell.db import Base, session
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship


class Project(Base):

    def __init__(self, team, name, description, proj_type, website=None,
                 status='unverified'):
        self.team = team
        self.name = name
        self.description = description
        self.type = proj_type
        self.website = website
        self.status = status

    def verify(self):
        self.status = 'verified'
        session.add(self)
        session.commit()

    def reject(self, reason):
        self.status = 'rejected'
        self.reject_reason = reason
        session.add(self)
        session.commit()

    @staticmethod
    def get_by_id(project_id):
        return session.query(Project).filter_by(project_id=project_id).one()

    def info_dict(self):
        return {
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'website': self.website,
            'repository': self.repository,
        }

    __tablename__ = 'projects'

    # Fields
    project_id = Column(Integer, autoincrement=True, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.team_id'), nullable=False)
    type = Column(String, nullable=False)
    description = Column(String)
    name = Column(String, unique=True, nullable=False)
    website = Column(String)
    repository = Column(String)
    status = Column(String, nullable=False, default="unverified")
    reject_reason = Column(String)

    # Constraints
    __table_args__ = (
        # Prevent rouge statuses
        CheckConstraint("status in ('unverified', 'rejected', 'verified')"),

        # Require reject reason if project is rejected
        CheckConstraint("reject_reason is not null or status != 'rejected'"),
    )

    # Relationships
    assets = relationship('ProjectAsset', cascade="all, delete-orphan", back_populates='project')
    team = relationship('Team', back_populates='projects')
