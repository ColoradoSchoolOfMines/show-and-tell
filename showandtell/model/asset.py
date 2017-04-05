#! /usr/bin/env python3

"""
Asset Model
"""

from showandtell.db import DeclarativeBase
from sqlalchemy import Column, Integer, String, Binary


class Asset(DeclarativeBase):
    __tablename__ = 'assets'

    # Fields
    asset_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    data = Column(Binary, nullable=False)
