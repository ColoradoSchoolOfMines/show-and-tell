#! /usr/bin/env python3

"""
Show and Tell
"""

from bottle import run
import showandtell

showandtell.db.Base.metadata.create_all()

run(host='localhost', port=8080, debug=True)
