from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField, PasswordField
from wtforms.validators import data_required, length
from flask_wtf.file import FileField
from datetime import date


class SearchForm(FlaskForm):
    search_text = StringField('Search...', validators=[data_required(), length(min=1, max=30)])
    submit1 = SubmitField('Search')


class AdvancedForm1(FlaskForm):
    search_text = StringField('Search...', validators=[data_required(), length(min=1, max=30)])
    beginning_time = StringField('Starting', validators=[data_required()])
    ending_time = StringField('Ending', validators=[data_required()])
    submit2 = SubmitField('Search')


class AdvancedForm2(FlaskForm):
    search_text = StringField('Search...', validators=[data_required(), length(min=1, max=30)])
    beginning_time = StringField('Starting', validators=[data_required()])
    ending_time = StringField('Ending', validators=[data_required()])
    graded = BooleanField('Graded', default=None)
    submit3 = SubmitField('Search')


class UploadForm(FlaskForm):
    file = FileField('')
    submit = SubmitField('Upload')


class LoginForm(FlaskForm):
    password = PasswordField('Password')
    submit = SubmitField('Login')