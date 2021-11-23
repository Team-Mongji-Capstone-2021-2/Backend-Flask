from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from wtforms import StringField, PasswordField, IntegerField

class CreateForm(FlaskForm):
    datafile = FileField('datafile',  validators=[FileRequired(), FileAllowed(['xls', 'xlsx', 'csv'], 'Excel Document only!')])
