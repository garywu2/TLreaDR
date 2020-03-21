from flask_restplus import Resource, fields, reqparse, marshal
from datetime import datetime
import uuid

from comment_service.api.restplus import api
from comment_service.models import db

ns = api.namespace('comments', description='Operations related to comments')