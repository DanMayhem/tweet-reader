#!python
'''user related models'''

import flask.ext.login

class User(flask.ext.login.UserMixin):
  def __init__(self, username):
    self.username = username

  def get_id(self):
    return self.username
