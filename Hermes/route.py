from Hermes import app
from flask import render_template, request, Response

@app.route('/')
def loginPage():
    return render_template('homePage.html')


@app.route('/sendVideo')
def sendVideoPage():

    return render_template('sendVideoPage.html')