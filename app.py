import re
import os
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from model.user_model import User
app = Flask(__name__)

app.secret_key="123123123"

# database 설정 파일
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:by1021md1024!@localhost:3307/capstone2"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route('/')
def home():
    #로그인 세션정보('username')가 있을 경우
	if not session.get('username'):  
		return render_template('home.html')

	#로그인 세션정보가 없을 경우
	else:
		return render_template('login.html')
		
	
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
    	return render_template('register.html')
    else:
	    username = request.form.get('username')
	    password = request.form.get('password')
	    name = request.form.get('name')
	    email = request.form.get('email')
	    gender = request.form.get('gender')
	    weight = request.form.get('weight')
	    height = request.form.get('height')

	    if not (username and password and name and email and gender and weight and height):
		    return "모두 입력해주세요"
	    else:
	        user = User()
	        user.username = username
	        user.password = password
	        user.name = name
	        user.email = email
	        user.gender = gender
	        user.weight = weight
	        user.height = height
	        db.session.add(user)
	        db.session.commit()
	        return "회원가입 완료"
	    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])	
def login():
	if request.method=='GET':
		return render_template('login.html')
	else:
		username = request.form['username']
		password = request.form['password']
		try:
			data = User.query.filter_by(username=username, password=password).first()	# ID/PW 조회Query 실행
			if data is not None:	# 쿼리 데이터가 존재하면
				session['username'] = username	# userid를 session에 저장한다.
				return render_template('home.html')
			else:
				return 'Dont Login'	# 쿼리 데이터가 없으면 출력
		except:
			return "dont login"	# 예외 상황 발생 시 출력

@app.route('/logout', methods=['GET'])
def logout():
	session.pop('username', None)
	return render_template('login.html')