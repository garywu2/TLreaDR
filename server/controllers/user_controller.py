from flask import jsonify
from flask_restplus import Resource

from server.api.restplus import api
from server.models.user import User

ns = api.namespace('users', description='Operations related to users')


@ns.route('/')
class UserList(Resource):
    def get(self):
        """
        Gets all registered users
        """
        results = User.query.all()
        return jsonify(results)
