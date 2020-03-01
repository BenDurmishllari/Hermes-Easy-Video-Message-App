from Hermes import app, firebase, auth, db, storage,UPLOAD_FOLDER
from flask import render_template, request, Response, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from Hermes.models import User
from flask_cors import CORS
from werkzeug.utils import secure_filename
from functools import wraps
import os
import json


# decorator to protect routes
# and verify that the user is
# register on the system and 
# it login normally
def isAuthenticated(s):
	@wraps(s)
	def decorated_function(*args, **kwargs):
		
		#check userId
		if not auth.current_user != None:
			return redirect(url_for('login'))
		return s(*args, **kwargs)
	return decorated_function

 
    

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():

	message = ""
	if request.method == "POST":
		
		
		email = request.form["LogInFormEmail"]
		password = request.form["LogInFormPassword"]
		
		loginUser = auth.sign_in_with_email_and_password(email, password)
		
		uidToken = loginUser['localId']
		uEmailToken = loginUser['email']
		
	
		getCurrentDB = db.child("Users").order_by_key().equal_to(uidToken).limit_to_first(1).get()
		if getCurrentDB != None:

			for gc in getCurrentDB.each():
				user = User(username = gc.val().get('username'),
						    email = gc.val().get('email'), 
							role = gc.val().get('role'), 
							userId = gc.val().get('userId'))

			if uidToken == user.get_userId():
				
				session['usrId'] = uidToken
				session["email"] = uEmailToken
				session["usrRole"] = user.get_role()
				session["usrUsername"] = user.get_username()
				print(user)
				print(session['usrId'])
				print(session["email"])
				print(session["usrRole"])
				print(session["usrUsername"])
			
			else:
				message = "Error!! Please Login Again"
				return redirect(url_for('login'))

		return redirect(url_for('home'))
	else:
			
		message = "Incorrect Password!"
	return render_template('loginPage.html')

#logout route
@app.route("/logout")
def logout():

	auth.curent_user = ""
	session.clear()
	return redirect("/")

	# try:
	# 	del session['usrId']
	# 	del session["email"]
	# 	del session["usrRole"]
	# 	del session["usrUsername"]
	# except KeyError:
	# 	session.clear()
	# return redirect("/");
   

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
@isAuthenticated
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
		data = {"username": username, "email": email, "role": role, "userId": currentUserId}
		createUserRef = db.child("Users").child(currentUserId).set(data)
		#db.child("Users").child(currentUserId).set(data)
		# UsercollectionReference.push(data)
		#UsercollectionReference.push(data, user['idToken'])
		
		return redirect(url_for('home'))
		
	return render_template('createAccountPage.html')

