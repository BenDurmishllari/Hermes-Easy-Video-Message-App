from flask import Flask, session
from flask_cors import CORS
#from werkzeug.utils import secure_filename
import pyrebase
import os
import config



app = Flask(__name__)
app.secret_key = os.urandom(24)


UPLOAD_FOLDER = './Hermes/static/uploadVideos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

# Config for the firebase
config = {
    
   ..keys..

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
#UsercollectionReference = db.child("Users")
storage = firebase.storage()

# path_on_cloud = "videos"
# path_on_local = "./Hermes/static/uploadVideos/myaudiovideo.mp4"
# storage.child(path_on_cloud).put(path_on_local)
# vide_url = storage.child(path_on_cloud).get_url()


# email = input('email\n')
# password = input('pass\n')

# user = auth.create_user_with_email_and_password(email, password)

# auth.get_account_info(user['idToken'])
# print(auth.get_account_info(user['idToken']))

# db = firebase.database()

# data = {
#     "name": "Mortimer 'Malaka' Malakas2"
# }

# results = db.child("users").push(data, user['idToken'])




from Hermes import route, models
from Hermes.models import User