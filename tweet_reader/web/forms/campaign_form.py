#!python

import flask.ext.wtf as w
import wtforms as f
import wtforms.validators as v
import wtforms.widgets

class CampaignForm(w.Form):
  search_key = f.StringField(
    'Search Key',
    validators=[
      v.InputRequired('Search Key is a required field')
    ],
  )

  longitude = f.DecimalField(
    'Latitude',
    validators=[
      v.
    ]
  )

  submit = f.SubmitField('Submit')
