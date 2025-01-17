# pylint: disable=missing-function-docstring, unused-argument, too-many-arguments
import functools

from flask import (
    Blueprint, g, redirect, session, url_for
)

from .services import UserService

"""
A Blueprint is a way to organize a group of views and other related codes. 
Rather than saving views and other codes directly in an application, they are saved in a blueprint. 
The blueprint is then registered with the application when it is available in the factory function.
https://flask-fr.readthedocs.io/tutorial/views/
"""

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = UserService.get_user_by_id()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view
