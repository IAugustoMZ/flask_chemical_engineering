from . import main
from flask import render_template

# define the error handlers
@main.app_errorhandler(404)
def page_not_found(e):
    """
    error handler for Error 404

    Parameters
    ----------
    e : object
        error 404 object
    """
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def page_not_found(e):
    """
    error handler for Error 500

    Parameters
    ----------
    e : object
        error 500 object
    """
    return render_template('500.html'), 500