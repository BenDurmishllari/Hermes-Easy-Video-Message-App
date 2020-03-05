from Hermes import (app, 
					firebase, 
					auth, 
					db, 
					storage, 
					UPLOAD_FOLDER, 
					login_manager)
from flask import (render_template, 
				   request, 
				   Response, 
				   redirect, 
				   url_for, 
				   session)
from flask_login import (login_user, 
                         logout_user, 
                         login_required, 
                         current_user)
from Hermes.models import User
from flask_cors import CORS
from werkzeug.utils import secure_filename
from functools import wraps
import os
import json






@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():

	message = ""

	if current_user.is_authenticated:
		return redirect(url_for('home'))

	if request.method == "POST":
		
		

		email = request.form["LogInFormEmail"]
		password = request.form["LogInFormPassword"]
		
		loginUser = auth.sign_in_with_email_and_password(email, password)
		
		uid = loginUser['localId']
		uEmailToken = loginUser['email']
		
	
		getCurrentDB = db.child("Users").order_by_key().equal_to(uid).limit_to_first(1).get()
		
		if getCurrentDB != None:

			for gc in getCurrentDB.each():
				user = User(username = gc.val().get('username'),
						    email = gc.val().get('email'), 
							role = gc.val().get('role'), 
							userId = gc.val().get('userId'),
							profile_image = gc.val().get('profile_image'))
			
			
			
			login_user(user)
			print(current_user)
			
		else:
			message = "No User found!"
		return redirect(url_for('home'))
	else:
			
		message = "Incorrect Password!"
	return render_template('loginPage.html')

#logout route
@app.route("/logout")
def logout():

	logout_user()

	return redirect(url_for('login'))
	
   

@app.route('/homePage', methods = ['GET', 'POST'])
@login_required
def home():
	
    return render_template('homePage.html')

@app.route('/createVideo', methods=['GET','POST'])
@login_required
def recordVideo():
	
    return render_template('createVideoPage.html')

@app.route('/watchVideo')
@login_required
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
# @login_required
def createAccount():
	
	if request.method == 'POST':
		
		email = request.form['CreateAccountFormEmail']
		password = request.form['CreateAccountFormPassword']
		username = request.form['CreateAccountFormUserName']
		role = request.form['CreateAccountFormRole']
		
		pic_file = request.files['userProfilePic']
		profile_pic = pic_file.read()

			
		user = auth.create_user_with_email_and_password(email, password)
		currentUserId = user['localId']
		currentUserEmail = user['email']
		
		put_pic = storage.child("profile_pic/" + str(currentUserEmail)).child(str(currentUserId)).put(profile_pic)
		#getCurrentPic = storage.child("profile_pic/" + str(currentUserEmail)).get_url(currentUserId)
		getCurrentPic = storage.child("profile_pic/" + str(currentUserEmail) + "/" + str(currentUserId)).get_url(str(currentUserId))
		data = {"username": username, 
				"email": email, 
				"role": role, 
				"userId": currentUserId, 
				"profile_image": getCurrentPic}
		
		createUserRef = db.child("Users").child(currentUserId).set(data)
		return redirect(url_for('home'))
		
	return render_template('createAccountPage.html')

@app.route('/usersPage', methods = ['GET', 'POST'])
# @login_required
def users():

	
	users = db.child("Users").get().val().values()
	
	
	return render_template('usersPage.html', users = users)
