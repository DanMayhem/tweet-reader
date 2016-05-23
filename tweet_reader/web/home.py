#!python
'''routes for main pages'''

import flask

from flask.ext.login import login_required, current_user

from ..campaigns import Campaign

from .forms import CampaignForm

bp = flask.Blueprint("home", __name__)

@bp.route("/", methods=['GET','POST'])
@bp.route("/index.html", methods=['GET','POST'])
@bp.route("/index", methods=['GET','POST'])
def index():
  if current_user.is_authenticated:
    campaign_form = CampaignForm()
    if campaign_form.validate_on_submit():
      c = Campaign()
      c.owner = current_user.username
      c.search = campaign_form.search_key.data
      c.latitude = campaign_form.latitude.data
      c.longitude = campaign_form.longitude.data
      c.radius = campaign_form.radius.data
      c.save()
      return flask.redirect(flask.url_for('.observe',key=c.key))
    return flask.render_template("home.html", form=campaign_form)
  return flask.render_template("landing.html")

@bp.route("/observe/<string:key>")
def observe(key):
  c = Campaign(key)
  if c is None:
    flask.flash('Invalid Campaign {key}'.format(key=key), 'danger')
    return flask.redirect(flask.url_for('.index'))
  flask.flash('campaign {key}'.format(key=c.key), 'success')
  return flask.render_template('observe.html', camp_key=key)
