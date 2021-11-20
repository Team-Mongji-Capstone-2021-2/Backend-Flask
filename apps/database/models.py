# -*- coding: utf-8 -*-
from datetime import datetime
import flask_login
from flask_sqlalchemy import SQLAlchemy
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



class EcgMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    local = db.Column(db.String(32))
    measured_date = db.Column(db.String(32))
    stress = db.Column(db.Boolean, default = False)
    arrhythmia = db.Column(db.Boolean, default = False)
    image_pc = db.Column(db.String(256))
    image_stress = db.Column(db.String(256))
    pac = db.Column(db.Boolean, default = False)
    pvc = db.Column(db.Boolean, default = False)
    rri_avg = db.Column(db.Integer, default = False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

class TestEcgModel(EcgMixin, db.Model):
    __tablename__ = 'test_ecg'

    user_id = db.Column(db.Integer(), db.ForeignKey('test_user.id'))

class EcgModel(EcgMixin, db.Model):
    __tablename__ = 'ecg'

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    test_model = TestEcgModel

Ecg = get_model(EcgModel)



class UserMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(32), unique=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    gender = db.Column(db.String(32), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(8), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified_date = db.Column(db.DateTime, nullable=True)

class TestUserModel(UserMixin, flask_login.UserMixin, db.Model):
    __tablename__ = 'test_user'

    ecg = db.relationship('TestEcgModel', backref = 'user')

class UserModel(UserMixin, flask_login.UserMixin, db.Model):
    __tablename__ = 'user'

    ecg = db.relationship('EcgModel', backref ='user')

    test_model = TestUserModel

User = get_model(UserModel)

@login_manager.user_loader
def member_loader(user_id):
    return User.query.filter(User.id == user_id).first()