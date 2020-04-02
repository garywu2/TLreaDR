from flask import Flask, Blueprint
from flask_cors import CORS

from server.api.restplus import api
from server.controllers.category_controller import ns as category_ns
from server.controllers.comment_controller import ns as comment_ns
from server.controllers.post_controller import ns as post_ns
from server.controllers.user_controller import ns as user_ns
from server.models import db
from .config import Config


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
    api.add_namespace(category_ns)
    api.add_namespace(comment_ns)
    api.add_namespace(post_ns)
    api.add_namespace(user_ns)

    '''Initialize models'''
    db.init_app(app)

    return app
