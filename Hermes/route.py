from Hermes import app, UPLOAD_FOLDER
from flask import render_template, request, Response, redirect
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os


@app.route('/')
def login():
	
    return render_template('loginPage.html')

@app.route('/homePage')
def home():
	
    return render_template('homePage.html')

@app.route('/createVideo', methods=['GET','POST'])
def recordVideo():
	
    return render_template('createVideoPage.html')

@app.route('/watchVideo')
def watchVideo():
		
    return render_template('watchVideoPage.html')




@app.route('/recordVideo',methods=['POST'])
def audiovideo():
	
	if request.method == 'POST':
		file = request.files['video']
		filename = "myaudiovideo.mp4"
		filename = secure_filename(filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return "success"




