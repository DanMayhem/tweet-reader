#!python
import html
import json
import time

import tweepy

from os import environ
from math import sin, cos, radians
from ..campaigns import find_campaign
from ..core import mongo, redis
from ..users import User

_RADIUS_OF_EARTH = 3959.0

class TweetStream(object):
  class _TweetReaderStreamListener(tweepy.StreamListener):
    def _skip_status(self, status):
      '''filters out statuses that are not in english, out of range or retweets'''
      if status.text.lower().startswith('rt'):
        return True

      #if self.cos_range == 0.0:
      #  return False #skip distance calc

      ##extract lat/long from tweet
      #if status.coordinates is None:
      #  return True

      #print ('has coords')

      #lat = radians(status.coordinates['coordinates'][0])
      #lon = radians(status.coordinates['coordinates'][1])
      #print("{0}:{1}".format(lat, lon))
      ##calculate cos_d
      #cos_d = self.sin_lat*sin(lat)+self.cos_lat*cos(lat)*cos(self.long_rad-lon)
      #if cos_d < self.cos_range:
      #  return True

      return False

    def on_status(self, status):
      if self._skip_status(status):
        return

      tweet_dict  = {
        'id': status.id,
        'text': html.unescape(status.text),
        'username': status.user.screen_name,
        'image_url': status.user.profile_image_url,
        'camp_key': self.camp_key,
      }
      mr = self.db.tweets.update_one(
        filter={
          'id': status.id,
          'camp_key': self.camp_key,
        },
        update={'$set': tweet_dict},
        upsert=True
      )

      if mr.upserted_id is not None:
        #publish tweet to redis
        self.redis.publish(self.camp_key, json.dumps(tweet_dict))

  def __init__(self, camp_key):
    #grab everything from the app context
    self.camp = find_campaign(camp_key)
    self.db = mongo.db
    self.redis = redis
    self.user = User(self.camp.owner)
    self.stream = None

  def __enter__(self):
    #load campaign
    if self.camp is None:
      return self

    #load the user who owns the campaign - the stream executes as them.
    if self.user.twitter_token is None:
      return self

    #create/initialize handler
    stream_listener = self._TweetReaderStreamListener()
    stream_listener.camp_key = self.camp.key
    stream_listener.db = self.db
    stream_listener.redis = self.redis
    stream_listener.cos_range = 0
    if self.camp.radius is not None:
      stream_listener.cos_range = cos(self.camp.radius/_RADIUS_OF_EARTH)
      stream_listener.sin_lat = sin(radians(self.camp.latitude))
      stream_listener.cos_lat = cos(radians(self.camp.latitude))
      stream_listener.long_rad = radians(self.camp.longitude)

    #authenticate
    auth = tweepy.OAuthHandler(
      environ.get('CONSUMER_KEY'),
      environ.get('CONSUMER_SECRET'),
    )

    #setup the stream
    auth.set_access_token(self.user.twitter_token, self.user.twitter_secret)
    api = tweepy.API(auth)
    self.stream = tweepy.Stream(auth=api.auth, listener = stream_listener)

    #start streaming
    self.stream.filter(
      track=[self.camp.search,],
      languages=['en',],
      async=True,
    )

    return self

  def __exit__(self, exc_type, exc_value, traceback):
    if self.stream is not None:
      self.stream.disconnect()
      self.stream = None

  def tweets(self, timeout=None):
    #generator to produce stream of tweets
    subscription = self.redis.pubsub()
    subscription.subscribe(self.camp.key)
    last_yield = time.time()
    with self:
      while True:
        msg = subscription.get_message()
        while msg is not None:
          if msg['type'] == 'message':
            yield msg['data']
            last_yield = time.time()
          msg = subscription.get_message()
        #when we get here we've drained the queue
        #sleep for 1 second (should be configurable)
        time.sleep(1)
        if (timeout is not None) and ((time.time() - last_yield) > timeout):
          #we haven't receive a message in a while, send a noop
          yield None
          last_yield = time.time()


  def event_stream(self):
    for t in self.tweets(5):
      if t is not None:
        yield "data: {tweet}\n\n".format(tweet=t.decode('utf-8'))
      else:
        yield "\n"

class TweetSearch(object):
  def __init__(self, camp_key):
    pass

  def tweets(self):
    pass

  def event_stream(self):
    pass
