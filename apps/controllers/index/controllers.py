from boto3 import session
from sqlalchemy import func
import pandas as pd
from datetime import datetime
from flask import Blueprint, render_template, redirect, request, url_for, abort
from wtforms.validators import Email
from apps.common.auth import api_signin_required, signin_required
from apps.controllers.index.forms import CreateForm
from flask_login import current_user
from apps.database.models import Ecg, User
from apps.database.session import db
from config import Config
from apps.common.response import ok, error
from werkzeug.utils import secure_filename
import os

from apps.service.pc_service import calculatePc

app = Blueprint('index', __name__, url_prefix='/index', static_url_path='/static')

@app.route('', methods=['GET'])
@signin_required
def index():
    args = request.args
    page = int(args.get('page') or 1)
    per_page = 1

    pagination1 = Ecg.query.filter(Ecg.user_id == current_user.id).order_by(Ecg.id.desc()).paginate(page, per_page, error_out=False)
    ecgs1 = pagination1.items

    ecgs2 = db.session.execute('select local as local, count(*) as count, count(case when stress = 1 then 1 end) as stress_count from ecg where ecg.user_id = :id group by local limit 5', {'id': current_user.id})

    #pagination3 = Datainfo.query.filter(Datainfo.user_id == current_user.id, Datainfo.arrhythmia == True).order_by(Datainfo.id.desc()).first()
    ecgs3 = db.session.execute('select * from ecg where ecg.user_id = :id and ecg.arrhythmia = 1 order by id desc', {'id': current_user.id});
    
    return render_template('home.html', ecgs1=ecgs1, pagination1=pagination1, ecgs2=ecgs2, ecgs3=ecgs3)

@app.route('/create', methods=['GET','POST'])
@signin_required
def create():
    form = CreateForm()

    if form.validate_on_submit():
        datafile = form.datafile.data
        datafile.save('./static/tmp_images/' + secure_filename(datafile.filename))
        data2 = pd.read_csv('./static/tmp_images/' + secure_filename(datafile.filename), encoding = 'utf-8', engine = 'python', index_col = False)
        os.remove('C:/Users/Pc/vsc/Backend-Flask/static/tmp_images/'+ secure_filename(datafile.filename))
        data2 = data2.drop(['박 헌'], axis = 1)
        data2 = data2[2511:-2500]
        data2 = data2.astype('float')
        data2.columns = [0]
        data2 = data2.reset_index()
        data2 = data2.drop(['index'], axis = 1)
        dates = ['2021-10-15 11:20:19']

        pc, pac, pvc, image_url = calculatePc(data2, dates)

        ecg = Ecg(local=form.local.data, user_id = current_user.id, pac = pac, pvc = pvc, arrhythmia=pc, image = image_url, measured_date=dates[0], created_date = datetime.now)
        db.session.add(ecg)
        db.session.commit()
        
        return redirect(url_for('index.index'))

    return render_template('create.html', form=form)


@app.route('/<int:ecg_id>', methods=['DELETE'])
@api_signin_required
def delete_data(ecg_id):
    ecg = Ecg.query.filter(Ecg.id == ecg_id).first()
    if not ecg:
        return error(40400)
    if current_user.id != ecg.user_id:
        return error(40300)

    db.session.delete(ecg)
    db.session.commit()
    return ok()