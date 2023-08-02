from flask import Blueprint

# define the main application blueprint
main = Blueprint('main', __name__)

# import routes and error definitions
from . import views, errors