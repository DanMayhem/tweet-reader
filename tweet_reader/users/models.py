#!python
'''user related models'''

import os

import flask_login

import tweepy

from ..core import mongo

class User(flask_login.UserMixin):
  def __init__(self, username):
    self.username = username
    self.twitter_token = None
    self.twitter_secret = None
    self.image_url = None
    u = mongo.db.users.find_one({'_id':username})
    if u is not None:
      self.twitter_token = u['twitter_token']
      self.twitter_secret = u['twitter_secret']
      if 'image_url' in u:
        self.image_url = u['image_url']

  def save(self):
    mongo.db.users.update_one(
      filter={'_id': self.username},
      update={'$set':{
        '_id': self.username,
        'twitter_token': self.twitter_token,
        'twitter_secret': self.twitter_secret,
        'image_url': self.image_url,
      }},
      upsert=True
    )

  def get_image_url(self):
    if self.image_url is None:
      self.fetch_twitter_details()
    return self.image_url

  def fetch_twitter_details(self):
      #fetch the latest image url from twitter
      auth = tweepy.OAuthHandler(
        os.environ.get('CONSUMER_KEY'),
        os.environ.get('CONSUMER_SECRET')
      )
      auth.set_access_token(self.twitter_token, self.twitter_secret)
      twitter = tweepy.API(auth)

      u = twitter.me()
      self.image_url = u.profile_image_url

  def get_id(self):
    return self.username
