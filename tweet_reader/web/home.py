#!python
'''routes for main pages'''

import flask

from flask.ext.login import login_required, current_user

from .forms import CampaignForm

bp = flask.Blueprint("home", __name__)

@bp.route("/", methods=['GET','POST'])
@bp.route("/index.html", methods=['GET','POST'])
@bp.route("/index", methods=['GET','POST'])
def index():
  if current_user.is_authenticated:
    campaign_form = CampaignForm()
    campaign_form.validate_on_submit()
    return flask.render_template("home.html", form=campaign_form)
  return flask.render_template("landing.html")
