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
import flask_login
import calendar
import time
import random





@login_manager.user_loader
def load_user(user_id):
    
    cUser = auth.current_user['localId']
	
    cUserDB = db.child("Users").child(cUser).get()
	
    user = User(username = cUserDB.val().get("username"),
                email = cUserDB.val().get("email"), 
                role = cUserDB.val().get("role"), 
                id = cUserDB.val().get("id"),
                profile_image = cUserDB.val().get("profile_image"))
	
    return user


# don't keep cache, any time it's play the current video
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



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
		
		user_id = loginUser['localId']
		uEmailToken = loginUser['email']
		
		getCurrentDB = db.child("Users").order_by_key().equal_to(user_id).limit_to_first(1).get()
		
		if getCurrentDB != None:

			for gc in getCurrentDB.each():
				user = User(username = gc.val().get('username'),
						    email = gc.val().get('email'), 
							role = gc.val().get('role'), 
							id = gc.val().get('id'),
							profile_image = gc.val().get('profile_image'))
		
			
			login_user(user)
			print(current_user)
			#print(session['_user_id'])
			# print("-------------login")
			# print(session)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			message = "No User found!"
		return redirect(url_for('login'))
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
	
	
	print(current_user)
	# print("homepage ----------------")
	# print(session)
	return render_template('homePage.html')

@app.route('/createVideo', methods=['GET','POST'])
# @login_required
def recordVideo():

	return render_template('createVideoPage.html')



@app.route('/watchVideo', methods=['GET','POST'])
# @login_required
def watchVideo():
	
	uid = current_user.get_id()
	ts = calendar.timegm(time.gmtime())
	 
	current_video = "./static/uploadVideos/" + str(uid) + ".mp4"
	# characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
	# result = ''
	# for i in range(0, 11):
	# 	result += random.choice(characters)	

	# if request.method == 'GET':
		
	# 	return redirect(url_for('watchVideo',result=result))


	if request.method == 'POST':
		if 'btnMakeOtherVideo' in request.form:
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'], str(uid) + ".mp4"))
			
			return redirect(url_for('recordVideo'))
	
	if request.method == 'POST':
		if 'btnSendVideo' in request.form:
		
			return redirect(url_for('users'))
			
	return render_template('watchVideoPage.html', current_video = current_video)


@app.route('/recordVideo',methods = ['GET','POST'])
def audiovideo():
	uid = current_user.get_id()
	ts = calendar.timegm(time.gmtime())

	if request.method == 'POST':
		file = request.files['video']
		filename = str(uid) + ".mp4"
		#filename = "myaudiovideo.mp4"
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
				"id": currentUserId, 
				"profile_image": getCurrentPic}
		
		createUserRef = db.child("Users").child(currentUserId).set(data)
		return redirect(url_for('home'))
		
	return render_template('createAccountPage.html')

@app.route('/users', methods = ['GET', 'POST'])
# @login_required
def users():

	cUser = current_user.get_id()
	users = db.child("Users").get().val().values()
	print(users)
		
	return render_template('usersPage.html',users = users)

@app.route('/sendMessage/<id>', methods = ['GET', 'POST'])
# @login_required
def sendMessage(id):

	receiver = db.child("Users").order_by_key().equal_to(id).limit_to_first(1).get()
	current_userId = current_user.get_id()
	current_video = "./Hermes/static/uploadVideos/" + str(current_userId) + ".mp4"

	timestamp = calendar.timegm(time.gmtime())
	#id = db.child("Users").child(id).get().val().get('id')
	#receiver = db.child("Users").child(id).get().val()
	for r in receiver:
		receiverId = r.val().get('id')
	if request.method == 'POST':
		if 'btnSendMessage' in request.form:
			# put_video = storage.child("Videos/" + str(current_userId) + "_" + str(receiverId)).child(str(current_userId) + "_" + str(receiverId)).put(current_video)
			#get_Video = storage.child("Videos/" + str(current_userId) + "_" + str(receiverId) + "/" + str(current_userId) + "_" + str(receiverId)).get_url(str(current_userId) + "_" + str(receiverId))
			
			
			test = "https://firebasestorage.googleapis.com/v0/b/hermes-d58c7.appspot.com/o/Videos%2FcPpoCCXnIvcAlZiTpWPoDlr5idY2_D2jDotkXctdhhNejE1sr43GvfXi2%2F1585270402%2FcPpoCCXnIvcAlZiTpWPoDlr5idY2_D2jDotkXctdhhNejE1sr43GvfXi2?alt=media&token=541c7078-164e-4993-842f-17f1337dbdb4"
			#put_video = storage.child("Videos/" + str(current_userId) + "_" + str(receiverId)).child(str(timestamp) + "/" +str(current_userId) + "_" + str(receiverId)).put(current_video)
			#get_Video = storage.child("Videos/" + str(current_userId) + "_" + str(receiverId) + "/").child(str(timestamp) +"/").get_url(str(current_userId) + "_" + str(receiverId))
			#print(get_Video)
			data = {
				
			}
			return redirect(url_for('watchVideo'))
			
	
	return render_template('sendMessagePage.html', receiver = receiver )


# path_on_cloud = "videos"
# path_on_local = "./Hermes/static/uploadVideos/myaudiovideo.mp4"
# storage.child(path_on_cloud).put(path_on_local)
# vide_url = storage.child(path_on_cloud).get_url()