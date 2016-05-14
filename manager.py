#!python
"""
Manager for flask-script
"""

import flask.ext.script

from tweet_reader.web import create_app

app = create_app()

manager = flask.ext.script.Manager(app)

if __name__=="__main__":
  manager.run()
