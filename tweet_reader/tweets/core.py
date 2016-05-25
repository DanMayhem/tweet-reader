#!python
import tweepy

from os import environ

from ..campaigns import find_campaign
from ..core import mongo
from ..users import User

class _StreamManager(object):
  class _TweetReaderStreamListener(tweepy.StreamListen):
    def on_status(self, status):
      mongo.db.update_one(
        filter={'id': status.id},
        update={'$set': {
          'id': status.id,
          'text': status.text,
          'username': status.user.screen_name,
          'image_url': status.user.profile_image_url,
          'camp_key': self.camp_key,
        }},
        upsert=True
      )

    def set_campaign(camp_key):
      self.camp_key = camp_key

  def __init__(self, camp_key):
    self.camp_key = camp_key
    self.stream = None

  def __enter__(self):
    #load campaign
    camp = find_campaign(camp_key)
    if camp is None:
      return self

    #load the user who owns the campaign - the stream executes as them.
    user = User(camp.owner)
    if user.twitter_token is None:
      return self

    #create/initialize handler
    stream_listener = _TweetReaderStreamListener()
    stream_listener.set_campaign(camp_key)

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
    self.stream.filter(track=camp.)

    return self

  def __exit__(self, exc_type, exc_value, traceback):
    if self.stream is not None:
      self.stream.disconnect()
      self.stream = None



def twitter_stream_generator(camp_key):
  with _StreamManager(camp_key) as tweet_stream:
    yield tweet_stream.get_next_tweet()
