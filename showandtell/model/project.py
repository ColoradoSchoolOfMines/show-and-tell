#! /usr/bin/env python3

"""
Project Model
"""

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Text
from sqlalchemy.orm import relation, synonym

project_table = Table('sat_project')
