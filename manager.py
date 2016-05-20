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

@manager.command
def list_camps():
  'print list of campaigns'
  for c in mongo.db.campaigns.find():
    print("{key} @{username}: '{search} [{lat}, {long}, {rad}]'".format({
      'key': c['_id'],
      'username': c['owner'],
      'search': c['search'],
      'lat': c['latitude'],
      'long': c['longitude'],
      'rad': c['radius'],
    }))

if __name__=="__main__":
  manager.run()
