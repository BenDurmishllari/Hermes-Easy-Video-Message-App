from flask import Flask
from flask_cors import CORS
#from werkzeug.utils import secure_filename
import pyrebase
import os
import config



app = Flask(__name__)
UPLOAD_FOLDER = './Hermes/static/uploadVideos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

# Config for the firebase
config = {
    ...project Keys etc...
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

email = input('email\n')
password = input('pass\n')

user = auth.create_user_with_email_and_password(email, password)

auth.get_account_info(user['idToken'])

# db = firebase.database()

# data = {
#     "name": "Mortimer 'Malaka' Malakas2"
# }

# results = db.child("users").push(data, user['idToken'])




from Hermes import route