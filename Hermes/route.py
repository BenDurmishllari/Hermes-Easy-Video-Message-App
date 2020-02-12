from Hermes import app, UPLOAD_FOLDER
from flask import render_template, request, Response
from werkzeug.utils import secure_filename
import os



# @app.route('/')
# def loginPage():
#     return render_template('homePage.html')


# @app.route('/sendVideo')
# def sendVideoPage():

#     return render_template('sendVideoPage.html')




@app.route('/', methods = ['GET', 'POST'])
def loginPage():

    
    
    return render_template('sendVideoPage.html')




@app.route('/audiovideo',methods=['GET', 'POST'])
def audiovideo():
	if request.method == 'POST':
		file = request.files['audiovideo']
		filename = "myaudiovideo.webm"
		filename = secure_filename(filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return "success"



