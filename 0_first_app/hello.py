import os
from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
from flask import Flask, render_template, session, redirect, url_for, flash

# define base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# app instance
app = Flask(__name__)

# configure secret key
app.config['SECRET_KEY'] = 'W&roN,ww%&hmEZ<'

# configure database information
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite') # connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # do not track modifications to save memory

# render hour and timestamp
moment = Moment(app)

# integrate with Bootstrap
bootstrap = Bootstrap(app)

# configure database
db = SQLAlchemy(app)

# define classes
# name form
class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[DataRequired()])
    submit = SubmitField('Submit')

# database tables
class Role(db.Model):
    # define table name and columns information
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    # string legible representation
    def __repr__(self):
        return '<Role %r>' % self.name
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

# define home route
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()                          # create class of form
    if form.validate_on_submit():              # validate submission
        old_name = session.get('name')         # extract old session name
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
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