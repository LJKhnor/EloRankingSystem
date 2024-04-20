"""The __init__.py serves double duty: it will contain the application factory, and it tells Python that the projet
directory should be treated as a package. Documentation :
https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/"""
# pylint: disable=missing-function-docstring,unused-argument,too-many-arguments,line-to-long
import os

from projet.views import *
from . import db, auth, business


def create_app(test_config=None):
    # create the my_app
    my_app = Flask(__name__, instance_relative_config=True)

    # create and configure the my_app
    my_app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(my_app.instance_path, 'project.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        my_app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        my_app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(my_app.instance_path)
    except OSError:
        pass
    #

    # initialize the my_app with the extension
    db.init_app(my_app)

    my_app.register_blueprint(auth.bp)
    my_app.register_blueprint(business.bp)

    my_app.add_url_rule("/", endpoint="index")
    my_app.add_url_rule("/league", endpoint="league")
    my_app.add_url_rule("/auth/login", endpoint="login")
    my_app.add_url_rule("/auth/signup", endpoint="signup")
    my_app.add_url_rule("/new_match", view_func=new_match)
    my_app.add_url_rule("/new_league", endpoint="new_league")
    my_app.add_url_rule("/rejeu", view_func=rejeu)

    return my_app
