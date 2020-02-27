from flask import Flask, Blueprint
from flask_cors import CORS

from .config import Config
from server.models import db
from server.api.restplus import api


def create_app():
    """Main wrapper for app creation"""
    app = Flask(__name__, static_folder='../build')
    app.config.from_object(Config)
    CORS(app)

    '''Initialize api and blueprint'''
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    '''Initialize models'''
    db.init_app(app)

    return app
