#! /usr/bin/env python3

""" Database Stuff """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from showandtell.helpers import util

__all__ = ['engine', 'Session', 'Base', 'session']

engine = create_engine(util.from_config_yaml('db'))

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
Base.metadata.bind = engine
