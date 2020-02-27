from flask import Flask, Blueprint
from flask_cors import CORS

from .config import Config
from server.database import db
from server.api.restplus import api

app = Flask(__name__, static_folder='../build')

def initialize_app(app):
    '''Main wrapper for app creation'''
    app.config.from_object(Config)
    CORS(app)

    '''Initialize api and blueprint'''
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    '''Initialize database'''
    db.init_app(app)

initialize_app(app)