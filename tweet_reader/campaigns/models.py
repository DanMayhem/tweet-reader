#!python

import random

from ..core import mongo

_key_chars = list("ABDEFGHJMNQRTYabdefghjmnqrty23456789")

def _gen_key():
  return ''.join([
    random.choice(_key_chars),
    random.choice(_key_chars),
    random.choice(_key_chars),
    random.choice(_key_chars),
    random.choice(_key_chars),
  ])

class Campaign(object):
  """docstring for Campaign"""
  def __init__(self, key=None):
    super(Campaign, self).__init__()

    self.key = key
    self.search = None
    self.latitude = None
    self.longitude = None
    self.radius = None
    self.owner = None

    if self.key is None:
      self.key = _gen_key()
      while (mongo.db.campaigns.find_one({'_id': self.key}) is not None):
        self.key = _gen_key()

    c = mongo.db.campaings.find_one({'_id': self.key})
    if c is not None:
      self.search = c['search']
      self.latitude = c['latitude']
      self.longitude = c['longitude']
      self.radius = c['radius']
      self.owner = c['owner']

  def save(self):
    mongo.db.campaigns.update_one(
      filter={'_id': self.key},
      update={'$set':{
        '_id': self.key,
        'search': self.search,
        'latitude': self.latitude,
        'longitude': self.longitude,
        'radius': self.radius,
        'owner': self.owner
      }},
      upsert=True
    )
