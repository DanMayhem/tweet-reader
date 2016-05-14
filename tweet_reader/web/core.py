#!python

#from flask_booststrap import Bootstrap

from ..core import create_app as parent_create_app
#from .static import bp as static_bp
#from .users import bp as users_bp

def create_app():
  app = parent_create_app(__name__)
  return app
