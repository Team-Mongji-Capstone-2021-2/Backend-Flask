from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user
import hashlib
from apps.common.auth import SHA256, already_signin
from apps.controllers.users.forms import SignInForm, SignUpForm
from apps.database.models import User
from apps.database.session import db

app = Blueprint('user', __name__, url_prefix='/user')


@app.route('/signin', methods=['GET', 'POST'])
@already_signin
def signin():
    form = SignInForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        print("username:", user.username, ", password: ", user.password)
        print("form_username:", form.username.data, ", form_password: ", form.password.data)
        print(SHA256.encrypt(form.password.data))
        if not user:
            form.username.errors.append('가입하지 않은 아이디 입니다.')
            return render_template('login.html', form=form)
        if user.password != SHA256.encrypt(form.password.data):
            form.password.errors.append('비밀번호가 일치하지 않습니다.')
            return render_template('login.html', form=form)

        login_user(user)
        return redirect(url_for('index.index'))
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
@already_signin
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        username_user = User.query.filter(User.username == form.username.data).first()
        password_user = User.query.filter(User.password == form.password.data).first()
        name_user = User.query.filter(User.name == form.name.data).first()
        email_user = User.query.filter(User.email == form.email.data).first()
        gender_user = User.query.filter(User.gender == form.gender.data).first()
        height_user = User.query.filter(User.height == form.height.data).first()
        weight_user = User.query.filter(User.weight == form.weight.data).first()

        if username_user:
            if username_user.username == form.username.data:
                form.username.errors.append('이미 가입된 아이디입니다.')

        if email_user:
            if email_user.email == form.email.data:
                form.email.errors.append('이미 가입된 이메일입니다.')

        if form.email.errors or form.username.errors:
            return render_template('register.html', form=form)
        user = User(username=form.username.data, password=SHA256.encrypt(form.password.data), name=form.name.data, email=form.email.data,
            gender=form.gender.data, height=form.height.data, weight=form.weight.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('index.index'))
    return render_template('register.html', form=form)


@app.route('/signout', methods=['GET'])
def signout():
    logout_user()
    return redirect(url_for('user.signin'))