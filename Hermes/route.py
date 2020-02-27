from Hermes import app, firebase, auth, db, storage, collectionReference,UPLOAD_FOLDER
from flask import render_template, request, Response, redirect, url_for, session
from Hermes.models import User
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():

	
	if request.method == 'POST':
		email = request.form['LogInFormEmail']
		password = request.form['LogInFormPassword']

		user = auth.sign_in_with_email_and_password(email, password)
		
		print(user['localId'])
		return redirect(url_for('home'))
		
	return render_template('loginPage.html')

@app.route('/homePage', methods = ['GET', 'POST'])
def home():
	
    return render_template('homePage.html')

@app.route('/createVideo', methods=['GET','POST'])
def recordVideo():
	
    return render_template('createVideoPage.html')

@app.route('/watchVideo')
def watchVideo():
		
    return render_template('watchVideoPage.html')




@app.route('/recordVideo',methods = ['POST'])
def audiovideo():
	
	if request.method == 'POST':
		file = request.files['video']
		filename = "myaudiovideo.mp4"
		filename = secure_filename(filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return "success"



@app.route('/createAccount', methods = ['GET', 'POST'])
def createAccount():
	
	if request.method == 'POST':
		
		email = request.form['CreateAccountFormEmail']
		password = request.form['CreateAccountFormPassword']
		username = request.form['CreateAccountFormUserName']
		role = request.form['CreateAccountFormRole']

			
		user = auth.create_user_with_email_and_password(email, password)
		currentUserId = user['localId']
		#users = User(username = username, email = email, role = role, userId = currentUserId)

		#data = {"username": users.get_username(), "email": users.get_email(), "role": users.get_role(), "uid": users.get_userId()}
		data = {"Username": username, "email": email, "role": role, "userId": currentUserId}
		collectionReference.push(data, user['idToken'])
		
		return redirect(url_for('home'))
		
	return render_template('createAccountPage.html')

