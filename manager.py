#!python
"""
Manager for flask-script
"""

import flask.ext.script

from tweet_reader import mongo
from tweet_reader.web import create_app
from tweet_reader.campaigns import find_campaign

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
    if 'latitude' not in c:
      c['latitude'] = 'n/a'
    if 'longitude' not in c:
      c['longitude'] = 'n/a'
    if 'radius' not in c:
      c['radius'] = 'n/a'
    print("{_id} @{owner}: '{search} [{latitude}, {longitude}, {radius}]'".format_map(c))

@manager.command
@manager.option('camp',help='campaign id')
def show_camp(camp):
  for tweet in mongo.db.tweets.find({'camp_key': camp}):
    print("@{username}\n{text}\n".format(**tweet))




if __name__=="__main__":
  manager.run()
