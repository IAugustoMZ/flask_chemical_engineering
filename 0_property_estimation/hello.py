from flask import Flask

# app instance
app = Flask(__name__)

# define home route
@app.route('/')
def index():
    return '<h1>Hello! Welcome to your Property Estimation Tool!</h1>'

# define user home page
@app.route('/user/<name>')
def user(name):
    return '<h2>Nice to have you back, {}!</h2>'.format(name)