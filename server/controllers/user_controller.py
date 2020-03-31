import requests
from flask import request
from flask_restplus import Resource

from server.models.api_models import *
from server.parsers.server_parsers import *

ns = api.namespace('users', description='Operations related to users routes')


@ns.route('')
class UserCollection(Resource):
    def get(self):
        """ Gets all users """
        response = requests.get('http://user_service:7082/api/users')
        return response.json(), response.status_code

    @ns.expect(user_model, validate=False)
    def post(self):
        """ Creates a new user """
        response = requests.post('http://user_service:7082/api/users', json=request.json)
        return response.json(), response.status_code


@ns.route('/<string:uuid>')
class UserItem(Resource):
    def get(self, uuid):
        """ Gets a specified user by uuid """
        response = requests.get('http://user_service:7082/api/users/' + uuid)
        return response.json(), response.status_code

    @ns.expect(user_put_model, validate=False)
    def put(self, uuid):
        """ Updates a user """
        response = requests.put('http://user_service:7082/api/users/' + uuid, json=request.json)
        return response.json(), response.status_code

    def delete(self, uuid):
        """ Deletes a user """
        response = requests.delete('http://user_service:7082/api/users/' + uuid)
        return response.json(), response.status_code


@ns.route('/login')
class UserLogin(Resource):
    @ns.expect(user_login_parser, validate=False)
    def get(self):
        """ Login for user """
        response = requests.get('http://user_service:7082/api/users/login', params=request.args)
        return response.json(), response.status_code
