import os
from app import create_app

# create the app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
