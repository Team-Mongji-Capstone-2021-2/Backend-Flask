from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장

class User(db.Model): #데이터 모델을 나타내는 객체 선언
    __tablename__ = 'user' #테이블 이름
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)
    gender = db.Column(db.String, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(8), nullable=False)
    #createdDate = db.Column(db.DateTime, default=datetime.utcnow())