"""
The __init__.py serves double duty: it will contain the application factory,
and it tells Python that the projet directory should be treated as a package.
Documentation : https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/
"""

import os

from flask import Flask
from projet.views import index

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # create and configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'projet.sqlite'),
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

    # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, and welcome to EloRankingSystem !'

    app.add_url_rule("/",view_func=index)

    return app