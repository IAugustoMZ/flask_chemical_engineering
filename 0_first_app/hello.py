from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
from flask import Flask, render_template, session, redirect, url_for

# app instance
app = Flask(__name__)

# configure secret key
app.config['SECRET_KEY'] = 'W&roN,ww%&hmEZ<'

# render hour and timestamp
moment = Moment(app)

# integrate with Bootstrap
bootstrap = Bootstrap(app)

# define classes
class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[DataRequired()])
    submit = SubmitField('Submit')

# define home route
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()                          # create class of form
    if form.validate_on_submit():              # validate submission
        session['name'] = form.name.data       # extract the name from form and save it on
                                               # session variable
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           current_time=datetime.utcnow())

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