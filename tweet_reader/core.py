#!python

from os import environ

import flask
import flask.ext.heroku

from flask.ext.login import LoginManager
from flask.ext.pymongo import PyMongo
from flask.ext.redis import FlaskRedis
from flask_oauthlib.client import OAuth
from flask_sslify import SSLify

login_manager = LoginManager()
oauth = OAuth()
mongo = PyMongo()
redis = FlaskRedis()

def create_app(package_name):
  app = flask.Flask(package_name)
  if "DEBUG_TWEET_READER" in environ:
    app.debug = True

  app.config['CSRF_ENABLED'] = True
  app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

  app.config['MONGO_URI'] = environ.get('MONGODB_URI')
  app.config['REDIS_URL'] = environ.get('REDIS_URL')
  #app.config['CONSUMER_KEY'] = environ.get('CONSUMER_KEY')
  #app.config['CONSUMER_SECRET'] = environ.get('CONSUMER_SECRET')


  flask.ext.heroku.Heroku(app)

  login_manager.init_app(app)
  oauth.init_app(app)
  mongo.init_app(app)
  redis.init_app(app)
  SSLify(app)

  return app
