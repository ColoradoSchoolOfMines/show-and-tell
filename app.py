#! /usr/bin/env python3

"""
Show and Tell
"""

import showandtell

from bottle import run

# Create the Database
showandtell.db.Base.metadata.create_all()

run(host='localhost', port=8080, debug=True)
