from flask_bootstrap import Bootstrap
from flask import Flask, render_template

# app instance
app = Flask(__name__)

# integrate with Bootstrap
bootstrap = Bootstrap(app)

# define home route
@app.route('/')
def index():
    return render_template('index.html')

# define user home page
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)