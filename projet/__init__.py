"""The __init__.py serves double duty: it will contain the application factory, and it tells Python that the projet
directory should be treated as a package. Documentation :
https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/"""

import os

from flask import Flask
from projet.views import *
from testElo import main
from . import db, auth, business


def create_app(test_config=None):
    # create the app
    app = Flask(__name__, instance_relative_config=True)

    # create and configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'project.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    #

    # initialize the app with the extension
    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(business.bp)

    app.add_url_rule("/", endpoint="index")
    app.add_url_rule("/league", endpoint="league")
    app.add_url_rule("/auth/login", endpoint="login")
    app.add_url_rule("/auth/signup", endpoint="signup")
    app.add_url_rule("/new_match", view_func=new_match)
    app.add_url_rule("/new_league", endpoint="new_league")
    app.add_url_rule("/rejeu", view_func=rejeu)

    return app
