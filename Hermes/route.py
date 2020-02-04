from Hermes import app
from flask import render_template

@app.route('/')
def loginPage():
    return render_template('homePage.html')


@app.route('/sendVideo', methods = ['GET', 'POST'])
def sendVideoPage():
    return render_template('sendVideoPage.html')