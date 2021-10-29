from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange


class SignInForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(message='필수 값입니다.'), 
                                                    Length(max=20, message='20자를 넘을 수 없습니다.')])
    password = PasswordField('password', validators=[DataRequired(message='필수 값입니다.'),
                                                     Length(max=20, message='20자를 넘을 수 없습니다.')])


class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(message='필수 값입니다.'),
                                                    Length(max=20, message='20자를 넘을 수 없습니다.')])
    password = PasswordField('password', validators=[DataRequired(message='필수 값입니다.'),
                                                     Length(max=20, message='20자를 넘을 수 없습니다.')])
    email = StringField('email', validators=[DataRequired(message='필수 값입니다.'),
                                                      Email(message='올바른 이메일 형식이 아닙니다.')])
    name = StringField('name', validators=[DataRequired(message='필수 값입니다.'),
                                                   Length(max=20, message='20자를 넘을 수 없습니다.')])
    height = IntegerField('height', validators=[DataRequired(message='필수 값입니다.'),
                                                   NumberRange(min=1, max=1000, message='3자를 넘을 수 없습니다.')])
    weight = IntegerField('weight', validators=[DataRequired(message='필수 값입니다.'),
                                                   NumberRange(min=1, max=1000, message='3자를 넘을 수 없습니다.')])
    gender = StringField('gender', validators=[DataRequired(message='필수 값입니다.'),
                                                   Length(max=2, message='2자를 넘을 수 없습니다.')])