#!python
'''routes for main pages'''

import flask

from flask.ext.login import login_required, current_user

bp = flask.Blueprint("home", __name__)

@bp.route("/")
@bp.route("/index.html")
@bp.route("/index")
def index():
  if current_user.is_authenticated:
    return flask.render_template("home.html")
  return flask.render_template("landing.html")
