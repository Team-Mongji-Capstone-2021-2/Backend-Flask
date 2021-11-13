# -*- coding: utf-8 -*-
from datetime import datetime

import flask_login

from apps.database.session import db, login_manager
from config import JsonConfig


def get_model(model):
    if JsonConfig.get_data('TESTING'):
        return model.test_model
    return model


class TestMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(120))


class TestTestModel(TestMixin, db.Model):
    __tablename__ = 'test_tests'


class TestModel(TestMixin, db.Model):
    __tablename__ = 'tests'

    test_model = TestTestModel


Test = get_model(TestModel)



class DatainfoMixin: #데이터 모델을 나타내는 객체 선언
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    local = db.Column(db.String(32))
    time = db.Column(db.String(32))
    stressData = db.Column(db.Boolean, default = False)
    arrhythmia = db.Column(db.Boolean, default = False)
    image = db.Column(db.String(256))
    pac = db.Column(db.Boolean, default = False)
    pvc = db.Column(db.Boolean, default = False)

class TestDatainfoModel(DatainfoMixin, db.Model):
    __tablename__ = 'test_datainfos'

    user_id = db.Column(db.Integer(), db.ForeignKey('test_users.id'))

class DatainfoModel(DatainfoMixin, db.Model):
    __tablename__ = 'datainfos'

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    test_model = TestDatainfoModel

Datainfo = get_model(DatainfoModel)



class UserMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(32), unique=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    gender = db.Column(db.String(32), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(8), nullable=False)

class TestUserModel(UserMixin, flask_login.UserMixin, db.Model):
    __tablename__ = 'test_users'

    datas = db.relationship('TestDatainfoModel', backref = 'user')

class UserModel(UserMixin, flask_login.UserMixin, db.Model):
    __tablename__ = 'users'

    datainfos = db.relationship('DatainfoModel', backref ='user')

    test_model = TestUserModel

User = get_model(UserModel)

@login_manager.user_loader
def member_loader(user_id):
    return User.query.filter(User.id == user_id).first()