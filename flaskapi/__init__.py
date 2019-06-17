import os

from flask import Flask
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from pathlib import Path  # python3 only

mongo = PyMongo()

def load_config(app, test_config):
    """ Loads configuration settings   """

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="default",
        # database settings
        MONGODB_DB='flaskydb',
        MONGODB_HOST='127.0.0.1',
        MONGODB_PORT=27017,
        MONGODB_USERNAME='flaskyuser',
        MONGODB_PASSWORD='secret'
    )

    if test_config is None:
        app.config.from_object('flaskapi.config.DevelopmentConfig')
    else:
        app.config.update(test_config)

    mongodb_connection_string = "mongodb://{0}:{1}@{2}:{3}/{4}".format(
        app.config.get('MONGODB_USERNAME'),
        app.config.get('MONGODB_PASSWORD'),
        app.config.get('MONGODB_HOST'),
        app.config.get('MONGODB_PORT'),
        app.config.get('MONGODB_DB')
    )
    app.config["MONGO_URI"] = mongodb_connection_string


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    load_config(app, test_config)

    mongo.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return "hello"

    # register auth api
    from flaskapi import auth
    app.register_blueprint(auth.bp)

    return app

