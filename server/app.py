from flask import Flask, Blueprint
from flask_cors import CORS

from server.api.restplus import api
from server.controllers.server_controller import ns as server_ns
from server.models import db
from .config import Config


def create_app():
    """Main wrapper for app creation"""
    app = Flask(__name__, static_folder='../build')
    app.config.from_object(Config)
    CORS(app)

    '''Initialize api and blueprint'''
    blueprint = Blueprint('api', __name__)
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    '''Loading api namespaces'''
    api.add_namespace(server_ns)

    '''Initialize models'''
    db.init_app(app)

    return app
