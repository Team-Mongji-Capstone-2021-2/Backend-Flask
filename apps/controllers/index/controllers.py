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

    pagination1 = Datainfo.query.filter(Datainfo.user_id == current_user.id).order_by(Datainfo.id.desc()).paginate(page, per_page, error_out=False)
    datainfos1 = pagination1.items

    datainfos2 = db.session.execute('select local as local, count(*) as count, count(case when stressData = 1 then 1 end) as stress_count from datainfos group by local limit 5')

    datainfos3 = Datainfo.query.filter(Datainfo.user_id == current_user.id, Datainfo.arrhythmia == True).order_by(Datainfo.id.desc()).limit(3)
    return render_template('home.html', datainfos1=datainfos1, pagination1=pagination1, datainfos2=datainfos2, datainfos3=datainfos3)

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

