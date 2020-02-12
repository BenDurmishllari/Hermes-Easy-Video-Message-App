from flask import Flask
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '../upload_files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)



from Hermes import route