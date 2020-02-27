from Hermes import app, firebase, auth, db, storage, collectionReference,UPLOAD_FOLDER
from flask import render_template, request, Response, redirect, url_for
from Hermes.models import User
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os


@app.route('/')
def login():
	
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
	currentUser = auth
	if request.method == 'POST':
		
		
		try:
			email = request.form['CreateAccountFormEmail']
			password = request.form['CreateAccountFormPassword']
			user = auth.create_user_with_email_and_password(email, password)
			data = {"name": "Mortimer 'Morty' Smith"}
			results = db.child("users").push(data, user['idToken'])
			return redirect(url_for('home'))
		except:
			print("Malakia")
	return render_template('createAccountPage.html')

