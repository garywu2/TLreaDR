from flask import Flask, Blueprint
from flask_cors import CORS

from .config import Config
from command_service.models import db
from command_service.api.restplus import api
from command_service.controllers.command_controller import ns as event_ns

def create_app():
    """Main wrapper for app creation"""
    app = Flask(__name__, static_folder='../build')
    app.config.from_object(Config)
    CORS(app)

    '''Initialize api and blueprint'''
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    '''Loading api namespaces'''
    api.add_namespace(event_ns)

    '''Initialize models'''
    db.init_app(app)

    return app
