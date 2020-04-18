from flask import Flask, session
from flask_cors import CORS
#from werkzeug.utils import secure_filename
import pyrebase
import os
import config
from flask_login import LoginManager




app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

login_manager = LoginManager(app)
# login_manager.init_app(app)

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

# path_on_cloud = "videos"
# path_on_local = "./Hermes/static/uploadVideos/cPpoCCXnIvcAlZiTpWPoDlr5idY2.mp4"
# storage.child(path_on_cloud).put(path_on_local)
# vide_url = storage.child(path_on_cloud).get_url()

from Hermes import route, models
from Hermes.models import User