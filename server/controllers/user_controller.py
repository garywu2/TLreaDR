from flask_restplus import Resource, fields, reqparse, marshal
from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from server.api.restplus import api
from server.models.user import User
from server.models import db

ns = api.namespace('users', description='Operations related to users')

user_dto = api.model('user', {
    'user_uuid': fields.String(required=True, description='user uuid'),
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
            return {"message": str(e)}, 500


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

        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        try:
            newUser = User(username, email, password)
            db.session.add(newUser)
            db.session.commit()
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'user has been created successfully.'}, 201


@ns.route('/delete')
class DeleteUser(Resource):

    user_delete_parser = reqparse.RequestParser()
    user_delete_parser.add_argument('username', required=True, type=str, help='username of user')

    @ns.expect(user_delete_parser)
    def delete(self):
        """
        Deletes a user
        """
        data = request.args

        username = data.get('username')

        try:
            userToBeDeleted = User.query.filter_by(username=username).first()
            if userToBeDeleted:
                db.session.delete(userToBeDeleted)
                db.session.commit()
            else:
                return {'message': 'user not found.'}, 404
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'user has been deleted successfully.'}, 201


@ns.route('/<string:username>')
class UserSearch(Resource):
    @ns.response(code=201, model=user_dto, description='Success')
    @ns.response(code=404, description='Not Found')
    def get(self, username):
        """
        Gets a specified user
        """
        try:
            queriedUser = User.query.filter_by(username=username).first()
            if queriedUser:
                return marshal(queriedUser, user_dto)
            else:
                return {"message": 'user not found'}, 404

        except Exception as e:
            return {"message": str(e)}, 500

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

        try:
            userToBeEditted = User.query.filter_by(username=username).first()

            if userToBeEditted:
                if data.get('new_email'):
                    userToBeEditted.email = data.get('new_email')
                if data.get('new_username'):
                    userToBeEditted.username = data.get('new_username')
                if data.get('new_password'):
                    userToBeEditted.password_hash = generate_password_hash(data.get('new_password'))
            else:
                return {'message': 'user specified not found in database'}, 201

            db.session.commit()
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'user has been edited successfully.'}, 201


@ns.route('/login')
class UserLogin(Resource):

    user_login_parser = reqparse.RequestParser()
    user_login_parser.add_argument('username', required=True, type=str, help='username of user')
    user_login_parser.add_argument('password', required=True, type=str, help='password of user')

    @ns.expect(user_login_parser)
    @ns.response(code=201, model=user_dto, description='Success')
    @ns.response(code=404, description='Not Found')
    def get(self):
        """
        Login a specified user
        """
        data = request.args

        input_username = data.get('username')
        input_password = data.get('password')

        try:
            queriedUser = User.query.filter_by(username=input_username).first()
            if queriedUser:
                if check_password_hash(queriedUser.password_hash, input_password):
                    return marshal(queriedUser, user_dto)
                else:
                    return {'message': 'invalid password'}, 404
            else:
                return {'message': 'username not found'}, 404

        except Exception as e:
            return {"message": str(e)}, 404






