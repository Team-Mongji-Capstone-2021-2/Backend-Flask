from flask import Blueprint, render_template, redirect, url_for
from apps.common.auth import SHA256, already_signin
from apps.controllers.users.forms import SignInForm, SignUpForm
from apps.database.models import User
from apps.database.session import db

app = Blueprint('main', __name__, url_prefix='/')

@app.route('', methods=['GET'])
def main():
    return redirect(url_for('user.signin'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.404.html'), 404