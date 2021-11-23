from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from wtforms import StringField, PasswordField, IntegerField

class CreateForm(FlaskForm):
    local = StringField('local', validators=[DataRequired(message='필수 값입니다.'),
                                                   Length(max=20, message='20자를 넘을 수 없습니다.')])
    datafile = FileField('datafile',  validators=[FileRequired(), FileAllowed(['xls', 'xlsx', 'csv'], 'Excel Document only!')])
