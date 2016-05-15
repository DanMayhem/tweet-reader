#!python
'''user related models'''

import flask.ext.login

from ..core import mongo

class User(flask.ext.login.UserMixin):
  def __init__(self, username):
    self.username = username
    self.twitter_token = None
    self.twitter_secret = None
    u = mongo.db.users.find_one({'_id':username})
    if u is not None:
      self.twitter_token = u['twitter_token']
      self.twitter_secret = u['twitter_secret']

  def save(self):
    mongo.db.users.update_one(
      filter={'_id': self.username},
      update={'$set':{
        '_id': self.username,
        'twitter_token': self.twitter_token,
        'twitter_secret': self.twitter_secret,
      }},
      upsert=True
    )

  def get_id(self):
    return self.username
