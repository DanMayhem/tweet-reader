#!python

'''suport for user related logic'''

from ..core import login_manager
from ..core import mongo

from .models import User

@login_manager.user_loader
def load_user(username):
  if mongo.db.users.find_one({'_id':username}) is not None:
    return User(username)
  return None
