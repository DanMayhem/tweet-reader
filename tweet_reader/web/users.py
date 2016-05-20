#!python
'''routes for user management'''

import os

import flask

from flask.ext.login import current_user, login_required

from ..core import oauth
from ..users import User

bp = flask.Blueprint('users', __name__)

twitter_oauth = oauth.remote_app(
  'twitter',
  request_token_url='https://api.twitter.com/oauth/request_token',
  access_token_url='https://api.twitter.com/oauth/access_token',
  authorize_url='https://api.twitter.com/oauth/authenticate',
  consumer_key=os.environ.get('CONSUMER_KEY'),
  consumer_secret=os.environ.get('CONSUMER_SECRET')
)

@bp.route('/')
def index():
  return flask.redirect(flask.url_for("home.index"))

@bp.route('/login')
def login():
  return twitter_oauth.authorize(callback=flask.url_for('.authorized'))

@login_required
@bp.route('/logout')
def logout():
  flask.ext.login.logout_user()
  flask.flash('Logged out.', 'success')
  return flask.redirect(flask.url_for('.index'))

@bp.route('/login_twitter_authorized')
def authorized():
  resp = twitter_oauth.authorized_response()
  if resp is None:
    flask.flash('login failed','danger')
  else:
    if isinstance(resp, Exception):
      raise resp
    u = User(resp['screen_name'])
    u.twitter_token = resp['oauth_token']
    u.twitter_secret = resp['oauth_token_secret']
    u.fetch_twitter_details()
    u.save()

    flask.ext.login.login_user(u, remember=True)

  return flask.redirect(flask.url_for('users.index'))

@twitter_oauth.tokengetter
def get_twitter_token(token=None):
  return (current_user.twitter_token, current_user.twitter_secret)
