#!python
import json
import tweepy

from os import environ
from ..campaigns import find_campaign
from ..core import mongo, redis
from ..users import User

class TweetStream(object):
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
    self.stream.filter(track=[self.camp.search,], async=True)

    return self

  def __exit__(self, exc_type, exc_value, traceback):
    if self.stream is not None:
      self.stream.disconnect()
      self.stream = None

  def tweets(self):
    #generator to produce stream of tweets
    subscription = self.redis.pubsub()
    subscription.subscribe(self.camp.key)
    with self:
      for msg in subscription.listen():
        if msg['type'] == 'message':
          yield msg['data']

  def event_stream(self):
    for t in self.tweets():
      yield "data: {tweet}\n\n".format(tweet=t.decode('utf-8'))
