#!python

from flask_bootstrap import Bootstrap

from ..core import create_app as parent_create_app
from .home import bp as home_bp
#from .users import bp as users_bp

def create_app():
  app = parent_create_app(__name__)

  Bootstrap(app)

  app.register_blueprint(home_bp)

  return app
