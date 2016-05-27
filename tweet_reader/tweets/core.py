#!python
import json
import tweepy

from os import environ
from ..campaigns import find_campaign
from ..core import mongo, redis
from ..users import User

class _StreamManager(object):
  class _TweetReaderStreamListener(tweepy.StreamListener):
    def on_status(self, status):
      tweet_dict  = {
        'id': status.id,
        'text': status.text,
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
    def set_campaign(self, camp_key):
      self.camp_key = camp_key

  def __init__(self, camp_key):
    self.camp_key = camp_key
    self.stream = None

  def __enter__(self):
    #load campaign
    camp = find_campaign(self.camp_key)
    if camp is None:
      return self

    #load the user who owns the campaign - the stream executes as them.
    user = User(camp.owner)
    if user.twitter_token is None:
      return self

    #create/initialize handler
    stream_listener = self._TweetReaderStreamListener()
    stream_listener.set_campaign(self.camp_key)
    stream_listener.db = mongo.db
    stream_listener.redis = redis

    #authenticate
    auth = tweepy.OAuthHandler(
      environ.get('CONSUMER_KEY'),
      environ.get('CONSUMER_SECRET'),
    )

    #setup the stream
    auth.set_access_token(user.twitter_token, user.twitter_secret)
    api = tweepy.API(auth)
    self.stream = tweepy.Stream(auth=api.auth, listener = stream_listener)

    #start streaming
    self.stream.filter(track=[camp.search,], async=True)

    return self

  def __exit__(self, exc_type, exc_value, traceback):
    if self.stream is not None:
      self.stream.disconnect()
      self.stream = None

def twitter_stream_generator(camp_key):
  pubsub = redis.pubsub()
  pubsub.subscribe(camp_key)
  with _StreamManager(camp_key) as tweet_stream:
    for msg in pubsub.listen():
      if msg['type'] == 'message':
        yield msg['data']
