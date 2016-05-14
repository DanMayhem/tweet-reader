#!python

from os import environ

import flask
import flask_sslify
import flask.ext.heroku
#import flask.ext.sqlalchemy

from flask.ext.login import LoginManager
from flask_oauthlib.client import OAuth

login_manager = LoginManager()
oauth = OAuth()

def create_app(package_name):
  app = flask.Flask(package_name)
  if "DEBUG_TWEET_READER" in environ:
    app.debug = True

  app.config['CSRF_ENABLED'] = True
  app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

  flask_sslify.SSLify(app)
  flask.ext.heroku.Heroku(app)

  login_manager.init_app(app)
  oauth.init_app(app)

  return app
