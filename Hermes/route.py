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
				   session,
				   flash,
				   abort)
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
import uuid
from collections import OrderedDict
from odict import odict
from datetime import datetime


# added
import hashlib
import base64


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

	
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	# if request.method == "POST":
		

	# 	email = request.form["LogInFormEmail"]
	# 	password = request.form["LogInFormPassword"]
		
	# 	loginUser = auth.sign_in_with_email_and_password(email, password)
		
	# 	user_id = loginUser['localId']
	# 	uEmailToken = loginUser['email']
		
	# 	getCurrentDB = db.child("Users").order_by_key().equal_to(user_id).limit_to_first(1).get()
		
	# 	if getCurrentDB != None:

	# 		for gc in getCurrentDB.each():
	# 			user = User(username = gc.val().get('username'),
	# 					    email = gc.val().get('email'), 
	# 						role = gc.val().get('role'), 
	# 						id = gc.val().get('id'),
	# 						profile_image = gc.val().get('profile_image'))
		
			
	# 		login_user(user)
	# 		print(current_user)
			
	# 		next_page = request.args.get('next')
	# 		return redirect(next_page) if next_page else redirect(url_for('home'))
	# 	else:
	# 		flash('Login Unsuccessful. Please check username and password', 'danger')
	# 	return redirect(url_for('login'))
	# else:
			
	if request.method == 'POST':
		
		email = request.form["LogInFormEmail"]
		password = request.form["LogInFormPassword"]
		
		try:
			
			loginUser = auth.sign_in_with_email_and_password(email, password)
			user_id = loginUser['localId']
			uEmailToken = loginUser['email']
			
			getCurrentDB = db.child("Users").order_by_key().equal_to(user_id).limit_to_first(1).get()
			
			for gc in getCurrentDB.each():
				user = User(username = gc.val().get('username'),
						    email = gc.val().get('email'), 
							role = gc.val().get('role'), 
							id = gc.val().get('id'),
							profile_image = gc.val().get('profile_image'))
				
				login_user(user, remember = True)
				print(current_user)
				
				next_page = request.args.get('next')
			
				return redirect(next_page) if next_page else redirect(url_for('home'))
		except:
			
			flash('Login Unsuccessful. Please check email and password', 'danger')
			return render_template('loginPage.html')
	
	return render_template('loginPage.html')

#logout route
@app.route("/logout")
def logout():

	logout_user()
	
	
	return redirect(url_for('login'))
	
   

@app.route('/homePage', methods = ['GET', 'POST'])
@login_required
def home():
	
	if request.method == 'POST':
		if 'btnInbox' in request.form:
			return redirect(url_for('inbox'))
	
	print(current_user)
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
		
		if 'btnSendVideo' in request.form:
		
			return redirect(url_for('users'))
	
	# if request.method == 'POST':
	# 	if 'btnSendVideo' in request.form:
		
	# 		return redirect(url_for('users'))
			
	return render_template('watchVideoPage.html', current_video = current_video)


@app.route('/recordVideo',methods = ['GET','POST'])
def audiovideo():
	uid = current_user.get_id()
	ts = calendar.timegm(time.gmtime())

	if request.method == 'POST':
		file = request.files['video']
		filename = str(uid) + ".mp4"
		# filename = "myaudiovideo.mp4"
		filename = secure_filename(filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return "success"
	




@app.route('/createAccount', methods = ['GET', 'POST'])
# @login_required
def createAccount():

	if current_user.get_role() != 'Admin':
		abort(403)
	
	if request.method == 'POST':
		
		email = request.form['CreateAccountFormEmail']
		password = request.form['CreateAccountFormPassword']
		username = request.form['CreateAccountFormUserName']
		role = request.form['CreateAccountFormRole']
		
		pic_file = request.files['userProfilePic']
		profile_pic = pic_file.read()

			
		# user = auth.create_user_with_email_and_password(email, password)
		# currentUserId = user['localId']
		# currentUserEmail = user['email']
		
		# put_pic = storage.child("profile_pic/" + str(currentUserEmail)).child(str(currentUserId)).put(profile_pic)
		# #getCurrentPic = storage.child("profile_pic/" + str(currentUserEmail)).get_url(currentUserId)
		# getCurrentPic = storage.child("profile_pic/" + str(currentUserEmail) + "/" + str(currentUserId)).get_url(str(currentUserId))
		# data = {"username": username, 
		# 		"email": email, 
		# 		"role": role, 
		# 		"id": currentUserId, 
		# 		"profile_image": getCurrentPic}
		
		# createUserRef = db.child("Users").child(currentUserId).set(data)
		# flash('Account has been created', 'success')
		# return redirect(url_for('home'))

		try:
			
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
			flash('Account has been created', 'success')
			return redirect(url_for('home'))
		
		except:
			
			flash('Something was wrong, try again please', 'danger')
			return render_template('createAccountPage.html')

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
	current_userName = current_user.get_username()
	current_userEmail = current_user.get_email()
	current_video = "./Hermes/static/uploadVideos/" + str(current_userId) + ".mp4"
	senderImageUrl = db.child("Users").child(current_userId).get().val().get('profile_image')
	


	for r in receiver:
		receiverId = r.val().get('id')
	
	if request.method == 'POST':
		if 'btnSendMessage' in request.form:

			with open(current_video, "rb") as f:
				file_hash = hashlib.md5()
				for chunk in iter(lambda: f.read(8192), b''): 
					print 
					file_hash.update(chunk)
			print (file_hash.digest()) #video that its on server
				# print (file_hash.hexdigest()) # debugging
	
			timestamp = calendar.timegm(time.gmtime())
			dt_object = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime(timestamp))

			try:
				# Uploads to firebase
				putVideo = storage.child("Videos/" + str(current_userId) + "_" + str(receiverId)).child(str(dt_object) + "/" + str(current_userId) + "_" + str(receiverId)).put(current_video)
				getVideoUrl = storage.child("Videos/" + str(current_userId) + "_" + str(receiverId)).child(str(dt_object) + "/" + str(current_userId) + "_" + str(receiverId)).get_url(str(current_userId) + "_" + str(receiverId))
				serverFile = file_hash.digest()
				firebaseStorageFile_Md5Hash = putVideo.get('md5Hash')
				firebaseStorageFile_digest = base64.b64decode(firebaseStorageFile_Md5Hash)


				data = {"sender_id": current_userId,
						"receiver_id": receiverId,
						"sender_name": current_userName,
						"sender_email": current_userEmail,
						"timestamp": dt_object, 
						"message_body": getVideoUrl,
						"profile_image": senderImageUrl}

				createMessage = db.child("Messages").child(receiverId).child(current_userId).child().push(data)

				current_message_dbTable_ID = createMessage.get('name')
		
				if serverFile == firebaseStorageFile_digest:
					os.remove(os.path.join(app.config['UPLOAD_FOLDER'], str(current_userId) + ".mp4"))
					print("13")
					flash('Video Message has been send it successfully', 'success')
					return redirect(url_for('home'))
				else:
					pass
					# return redirect(url_for('resendMessage', receiver_id = receiverId))
			except:
				return redirect(url_for('resendMessage', receiver_id = receiverId))
				

		
		if 'btnBackChooseOtherUser' in request.form:
			return redirect(url_for('users'))
			
	
	return render_template('sendMessagePage.html', receiver = receiver )

@app.route('/resendMessage%r=<receiver_id>', methods = ['GET', 'POST'])
# @login_required
def resendMessage(receiver_id):
	
	current_userId = current_user.get_id()
	current_userName = current_user.get_username()
	current_userEmail = current_user.get_email()
	current_video = "./Hermes/static/uploadVideos/" + str(current_userId) + ".mp4"
	replay_video = "./static/uploadVideos/" + str(current_userId) + ".mp4"
	senderImageUrl = db.child("Users").child(current_userId).get().val().get('profile_image')
	receiverId = db.child("Users").order_by_key().equal_to(receiver_id).limit_to_first(1).get()

	for r in receiverId:
		r_Id = r.val().get('id')

	if request.method == 'POST':
		if 'btnResendMessage' in request.form:

			timestamp = calendar.timegm(time.gmtime())
			dt_object = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime(timestamp))

			
			# Uploads to firebase
			putVideo = storage.child("Videos/" + str(current_userId) + "_" + str(r_Id)).child(str(dt_object) + "/" + str(current_userId) + "_" + str(r_Id)).put(current_video)
			getVideoUrl = storage.child("Videos/" + str(current_userId) + "_" + str(r_Id)).child(str(dt_object) + "/" + str(current_userId) + "_" + str(r_Id)).get_url(str(current_userId) + "_" + str(r_Id))

			data = {"sender_id": current_userId,
					"receiver_id": r_Id,
					"sender_name": current_userName,
					"sender_email": current_userEmail,
					"timestamp": dt_object, 
					"message_body": getVideoUrl,
					"profile_image": senderImageUrl}

			createMessage = db.child("Messages").child(r_Id).child(current_userId).child().push(data)
			flash('Video Message has been send it successfully', 'success')
			return redirect(url_for('home'))

	# q = "-M5-GjWImIokXaEFVfOC"
	# v = db.child("Messages").child("D2jDotkXctdhhNejE1sr43GvfXi2").child("cPpoCCXnIvcAlZiTpWPoDlr5idY2").get()
	# l = []
	# for s in v:
	# 	msgId = s.key()
	# 	l.append(msgId)
	# for i in l:
	# 	if q not in l:
	# 		print("dont exist")
	# 	else:
	# 		print("exist")
		

	
	return render_template('emergencyMessagePage.html', pending_video = replay_video)


@app.route('/inbox', methods = ['GET', 'POST'])
# @login_required
def inbox():
	
	current_userId = current_user.get_id()
	
	current_userMessages = db.child("Messages").child(current_userId)

	try:

		data = {}
		for s in current_userMessages.get():
			senderId = s.key()
			sender = db.child("Messages").child(current_userId).child(senderId)
			
			for msgId in sender.get():
				messageId = msgId.key()
				
				messages = db.child("Messages").child(current_userId).child(senderId).child(messageId).get()
				
				data[messageId] = dict(messages.val())
	
		print(data)
		
	except:
		noMsg = 'You don\'t have any video message yet.'
		flash('No messages', 'danger')
		return render_template('inboxPage.html', noMsg=noMsg)
	return render_template('inboxPage.html', messages=data)


@app.route('/watchVideoMessage/s=<senderId>%M=<msgId>', methods = ['GET', 'POST'])
# @login_required
def watchVideoMessage(senderId, msgId):
	
	current_userId = current_user.get_id()
	reiceivedMessage = db.child("Messages").child(current_userId).child(senderId).order_by_key().equal_to(msgId).limit_to_first(1).get()
	
	if request.method == 'POST':
		if 'btnBackInbox' in request.form:
			return redirect(url_for('inbox'))
		if 'btnBackMainMenu' in request.form:
			return redirect(url_for('home'))
	

	
			
	
	return render_template('watchVideoMessagePage.html', videoMessage = reiceivedMessage)
