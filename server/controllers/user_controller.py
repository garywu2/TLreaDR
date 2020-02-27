from flask_restplus import Resource, fields

from server.api.restplus import api
from server.models.user import User

ns = api.namespace('users', description='Operations related to users')

user_dto = api.model('user', {
    'email': fields.String(required=True, description='user email address'),
    'username': fields.String(required=True, description='user username'),
})


@ns.route('/')
class UserList(Resource):
    @ns.marshal_list_with(user_dto)
    def get(self):
        """
        Gets all registered users
        """
        results = User.query.all()
        return results
