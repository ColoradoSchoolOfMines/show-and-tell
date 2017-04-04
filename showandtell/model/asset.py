#! /usr/bin/env python3

"""
Asset Model
"""

from showandtell.db import DeclarativeBase, session
from sqlalchemy import Column, Integer, String, Binary
from sqlalchemy.orm import relationship


class Asset:
    __tablename__ = 't_assets'

    # Fields
    asset_id = Column(Integer, autoincrement=True, primary_key=True)
    project_id = Column(Integer)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    data = Column(Binary, nullable=False)
