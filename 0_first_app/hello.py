import os
from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_migrate import Migrate
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

# implement database migrations manager
migrate = Migrate(app, db)

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
        
        # query user from database
        user = User.query.filter_by(username=form.name.data).first()

        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
            session['name'] = form.name.data
            form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                            form=form, name=session.get('name'),
                            known=session.get('known', False),
                            current_time=datetime.now())

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

# add a shell context integration
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)