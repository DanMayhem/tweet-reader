#!python

from os import environ

import flask
import flask.ext.heroku

from flask.ext.login import LoginManager
from flask.ext.pymongo import PyMongo
from flask_oauthlib.client import OAuth

login_manager = LoginManager()
oauth = OAuth()
mongo = PyMongo()

def create_app(package_name):
  app = flask.Flask(package_name)
  if "DEBUG_TWEET_READER" in environ:
    app.debug = True

  app.config['CSRF_ENABLED'] = True
  app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

  app.config['MONGO_URI'] = environ.get('MONGODB_URI')
  #app.config['CONSUMER_KEY'] = environ.get('CONSUMER_KEY')
  #app.config['CONSUMER_SECRET'] = environ.get('CONSUMER_SECRET')


  flask.ext.heroku.Heroku(app)

  login_manager.init_app(app)
  oauth.init_app(app)
  mongo.init_app(app)

  return app
