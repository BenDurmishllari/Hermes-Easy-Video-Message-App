from Hermes import app
from flask import render_template

@app.route('/')
def loginPage():
    return render_template('index.html')