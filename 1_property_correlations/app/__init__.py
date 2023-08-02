from config import config
from flask_mail import Mail
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

# prepare classes for building
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

# create app function
def create_app(config_name: str) -> Flask:
    """
    creates a factory of the application

    Parameters
    ----------
    config_name : str
        configuration string

    Returns
    -------
    Flask
        flask app
    """
    app = Flask(__name__)

    # import configuration
    app.config.from_object(config[config_name])

    # initialize configuration
    config[config_name].init_app(app)

    # initialize support classes
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # import and register the blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app