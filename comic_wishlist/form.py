from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import data_required, length


class SearchForm(FlaskForm):
    search_text = StringField('Search...', validators=[data_required(), length(min=1, max=30)])
    submit = SubmitField('Search')

