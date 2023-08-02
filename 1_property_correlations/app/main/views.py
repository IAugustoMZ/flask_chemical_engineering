from . import main
from flask import render_template

# define the routes
@main.route('/',
            methods=['GET', 'POST'])
def index():
    return '<h1>Hello World!</h1>'
    # return render_template('index.html')