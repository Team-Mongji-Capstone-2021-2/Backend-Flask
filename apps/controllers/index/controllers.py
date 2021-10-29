from boto3 import session
from sqlalchemy import func
import pandas as pd
from flask import Blueprint, render_template, redirect, request, url_for
from apps.common.auth import signin_required
from apps.controllers.index.forms import CreateForm
from flask_login import current_user
from apps.database.models import Datainfo, User
from apps.database.session import db
from config import Config

from apps.service.pac_service import calculatePac

app = Blueprint('index', __name__, url_prefix='/index')

@app.route('', methods=['GET'])
@signin_required
def index():
    args = request.args
    page = int(args.get('page') or 1)
    per_page = 1

    pagination1 = Datainfo.query.order_by(Datainfo.id.desc()).paginate(page, per_page)
    datainfos1 = pagination1.items

    #datainfos2 = db.session.query(Datainfo, db.func.count(Datainfo.local)).group_by(Datainfo.local)
    pagination2 = db.session.query(Datainfo.local, func.count('*')).group_by(Datainfo.local).paginate(page, per_page);
    #pagination2 = Datainfo.query.order_by((Datainfo.func.count(Datainfo.local)).decs()).paginate(page, per_page)
    datainfos2 = pagination2.items

    return render_template('home.html', datainfos1=datainfos1, pagination1=pagination1, datainfos2=datainfos2, pagination2=pagination2)


@app.route('/create', methods=['GET','POST'])
@signin_required
def create():
    form = CreateForm()

    if form.validate_on_submit():
        local_datainfo = Datainfo.query.filter(Datainfo.local == form.local.data).first()
        datafile = form.datafile.data
        data = pd.read_csv(datafile)
        print(data)
        image_url, pac = calculatePac()

        datainfo = Datainfo(local=form.local.data, user_id = current_user.id, pac = pac, image = image_url)
        db.session.add(datainfo)
        db.session.commit()
        
        return redirect(url_for('index.index'))
    return render_template('create.html', form=form)
