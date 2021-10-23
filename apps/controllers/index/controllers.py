import re
from datetime import datetime, timedelta

from flask import Blueprint, render_template, request
from flask_login import current_user

from apps.common.auth import signin_required, already_signin
from apps.database.models import Data
from apps.database.session import db
from config import Config

app = Blueprint('index', __name__, url_prefix='/index')


@app.route('', methods=['GET'])
@already_signin
#@signin_required
def index():
    datas = Data.query.all()
    return render_template('home.html', datas=datas)


@app.route('/create', methods=['GET'])
@already_signin
def create():
    return render_template('create.html')