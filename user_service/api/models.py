from flask_restplus import fields

from user_service.api.restplus import api

user_dto = api.model('user', {
    'user_uuid': fields.String(required=True, description='user uuid'),
    'email': fields.String(required=True, description='user email address'),
    'username': fields.String(required=True, description='user username'),
    'is_admin': fields.Boolean(required=True, description='true if user is an admin'),
})
