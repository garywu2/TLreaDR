import logging

from flask import Flask, Blueprint
from flask_cors import CORS

from .config import Config
from server.models import db
from server.api.restplus import api

from server.controllers.user_controller import ns as user_ns

def create_app():
    """Main wrapper for app creation"""
    logging.basicConfig(level=logging.DEBUG)
    app = Flask(__name__, static_folder='../build')
    app.config.from_object(Config)
    CORS(app)

    '''Initialize api and blueprint'''
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    '''Loading api namespaces'''
    api.add_namespace(user_ns)

    '''Initialize models'''
    db.init_app(app)

    return app
