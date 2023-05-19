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

# define customized error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500