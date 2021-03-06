from flask import Flask, session
from flask_cors import CORS
import pyrebase
import os
import config
from flask_login import LoginManager




app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

login_manager = LoginManager(app)


login_manager.login_view = 'login'

login_manager.login_message_category = 'info'



UPLOAD_FOLDER = './Hermes/static/uploadVideos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

# Config for the firebase
config = {
    
   ...keys...

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

storage = firebase.storage()

from Hermes import route, models
from Hermes.models import User