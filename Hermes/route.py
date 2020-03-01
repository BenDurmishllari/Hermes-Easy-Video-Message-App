from Hermes import app, firebase, auth, db, storage, collectionReference,UPLOAD_FOLDER
from flask import render_template, request, Response, redirect, url_for, session
from Hermes.models import User
#from flask_login import login_user, logout_user, login_required, current_user
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():


	message = ""
	if request.method == "POST":
		
		
		email = request.form["LogInFormEmail"]
		password = request.form["LogInFormPassword"]
		
		loginUser = auth.sign_in_with_email_and_password(email, password)
		#print(auth.current_user)
		#print("------------------")
		#user_id = loginUser['idToken']
		#print(loginUser)
		#docRef = collectionReference.get()
		
		#print(docRef)
		# if docRef != None:
		# 	for dc in docRef.each():
		# 		user = User(username = dc.val().get('Username'), email = dc.val().get('email'), role = dc.val().get('role'), userId = dc.val().get('userId'))
		# 		# user.set_username(dc.val().get('username'))
		# 		# user.set_email(dc.val().get('email'))
		# 		# user.set_role(dc.val().get('role'))
		# 		# user.set_userId(dc.val().get('userId'))

		# 		print(user)
		
		
		# print(user.get('localId'))
		# print(user)
		#user = auth.refresh(user['refreshToken'])
		#user_id = user['idToken']
		#oeo = auth.get_account_info(user['idToken'])
		#print(oeo)
		#print("----------")
		#print(user)
		#session['usr'] = user_id
		#print("----------")
		#print(session['usr'])
	# 	return redirect(url_for('home'))
	else:
			
		message = "Incorrect Password!"
	return render_template('loginPage.html')

	# if request.method == 'POST':
		
	# 	email = request.form['LogInFormEmail']
	# 	password = request.form['LogInFormPassword']

	# 	user = auth.sign_in_with_email_and_password(email, password)
	# 	db.child("users").shallow().get()

	# 	if auth.current_user == users['localId']:
	# 		login_user(user)


	
	# if request.method == 'POST':
	# 	email = request.form['LogInFormEmail']
	# 	password = request.form['LogInFormPassword']

	# 	user = auth.sign_in_with_email_and_password(email, password)
	# 	#user_id = auth.get_account_info(user['idToken'])
	# 	#session['usr'] = user_id

	# 	current_user = user['localId']
	# 	print(current_user + " " + "edw malaka")

	# 	if auth.current_user:
	# 		print(auth.current_user)

	# 	# print(user)
	# 	# print("-------------------------------------")
	# 	# print(user['idToken'])
		

	# 	# users = db.child("Users").shallow().get()
	# 	# print(users.val())

	# 	all_users = db.child("Users").get()
	# 	for userr in all_users.each():
	# 		print("----------------")
	# 		print(userr.key()) 
	# 		print("----------------")
	# 		print(userr.val())
	# 		print("----------------")
	# 		print(userr.val().get('userId'))
	# 		print("----------------")
		

		
		
	# 	print(user['localId'])
	# 	return redirect(url_for('home'))
	
	# users = db.child("Users").get()
	# print(users.val()) 
		
	# return render_template('loginPage.html')

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
		data = {"username": username, "email": email, "role": role, "userId": currentUserId}
		collectionReference.push(data)
		#collectionReference.push(data, user['idToken'])
		
		return redirect(url_for('home'))
		
	return render_template('createAccountPage.html')

