#!python
"""
Manager for flask-script
"""

import flask.ext.script

from tweet_reader import mongo
from tweet_reader.web import create_app

app = create_app()

manager = flask.ext.script.Manager(app)

@manager.command
def list_users():
  'print list of registered users'
  for u in mongo.db.users.find():
    print("@{username}".format(username=u['_id']))

if __name__=="__main__":
  manager.run()
