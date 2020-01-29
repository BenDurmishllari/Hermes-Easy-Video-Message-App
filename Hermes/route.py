from Hermes import app

@app.route('/')
def hello():
    return "Hello Hermes"