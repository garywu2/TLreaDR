from flask_restplus import Resource, fields, reqparse
from flask import request, make_response

from server.api.restplus import api
from server.models.user import User
from server.models import db

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
        try:
            results = User.query.all()
            return results
        except Exception as e:
            return make_response({"message": str(e)}, 500)


@ns.route('/add')
class AddUser(Resource):

    user_add_parser = reqparse.RequestParser()
    user_add_parser.add_argument('email', required=True, type=str, help='email of user')
    user_add_parser.add_argument('username', required=True, type=str, help='username of user')
    user_add_parser.add_argument('password', required=True, type=str, help='password of user')

    @api.expect(user_add_parser)
    def post(self):
        """
        Adds a new user
        """
        data = request.args

        email = data['email']
        username = data['username']
        password = data['password']

        try:
            newUser = User(username, email, password)
            db.session.add(newUser)
            db.session.commit()
        except Exception as e:
            return make_response({"message": str(e)}, 500)

        return make_response({'message': 'user has been created successfully.'}, 201)


@ns.route('/delete')
class DeleteUser(Resource):

    user_delete_parser = reqparse.RequestParser()
    user_delete_parser.add_argument('username', required=True, type=str, help='username of user')

    @ns.expect(user_delete_parser)
    def post(self):
        """
        Deletes a user
        """
        data = request.args

        username = data['username']

        try:
            userToBeDeleted = User.query.filter_by(username=username).first()
            db.session.delete(userToBeDeleted)
            db.session.commit()
        except Exception as e:
            return make_response({"message": str(e)}, 500)

        return make_response({'message': 'user has been deleted successfully.'}, 201)


@ns.route('/<string:username>')
class UserSearch(Resource):
    @ns.marshal_list_with(user_dto)
    def get(self, username):
        """
        Gets a specified user
        """
        try:
            results = User.query.filter_by(username=username).first()
            return results
        except Exception as e:
            return make_response({"message": str(e)}, 500)

    user_edit_parser = reqparse.RequestParser()
    user_edit_parser.add_argument('new_email', nullable=True, required=False, type=str, help='new email of user')
    user_edit_parser.add_argument('new_username', nullable=True, required=False, type=str, help='new username of user')
    user_edit_parser.add_argument('new_password', nullable=True, required=False, type=str, help='new password of user')

    @ns.expect(user_edit_parser)
    def put(self, username):
        """
        Updates an existing user's information
        """
        data = request.args

        new_email = data['new_email']
        new_username = data['new_username']
        new_password = data['new_password']

        try:
            userToBeEditted = User.query.filter_by(username=username).first()

            if new_email:
                userToBeEditted.email = data['new_email']
            if new_username:
                userToBeEditted.username = data['new_username']
            if new_password:
                userToBeEditted.password = data['new_password']

            db.session.commit()
        except Exception as e:
            return make_response({"message": str(e)}, 500)

        return make_response({'message': 'user has been editted successfully.'}, 201)









