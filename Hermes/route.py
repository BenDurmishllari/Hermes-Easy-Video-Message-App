from Hermes import app, UPLOAD_FOLDER
from flask import render_template, request, Response, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os




# @app.route('/')
# def loginPage():
#     return render_template('homePage.html')


# @app.route('/sendVideo')
# def sendVideoPage():

#     return render_template('sendVideoPage.html')



@app.route('/')
def loginPage():
	
    return render_template('sendVideoPage.html')




@app.route('/audiovideo',methods=['POST'])
def audiovideo():
	
	if request.method == 'POST':
		file = request.files['audiovideo']
		filename = "myaudiovideo.mp4"
		filename = secure_filename(filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return "success"




