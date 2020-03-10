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


user_add_parser = reqparse.RequestParser()
user_add_parser.add_argument('email', required=True, type=str, help='email of user', location='json')
user_add_parser.add_argument('username', required=True, type=str, help='username of user', location='json')
user_add_parser.add_argument('password', required=True, type=str, help='password of user', location='json')

@ns.route('/add')
class AddUser(Resource):

    @api.expect(user_add_parser)
    def post(self):
        """
        Adds a new user
        """
        args = user_add_parser.parse_args()

        try:
            new_user = User(args['username'], args['email'], args['password'])
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'user has been created successfully.'}, 201

user_delete_parser = reqparse.RequestParser()
user_delete_parser.add_argument('username', required=True, type=str, help='username of user', location='json')

@ns.route('/delete')
class DeleteUser(Resource):

    @ns.expect(user_delete_parser)
    def delete(self):
        """
        Deletes a user
        """
        args = user_delete_parser.parse_args()

        try:
            user_to_be_deleted = User.query.filter_by(username=args['username']).first()
            if user_to_be_deleted:
                db.session.delete(user_to_be_deleted)
                db.session.commit()
            else:
                return {'message': 'user not found.'}, 404
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'user has been deleted successfully.'}, 201

user_edit_parser = reqparse.RequestParser()
user_edit_parser.add_argument('new_email', nullable=True, required=False, type=str, help='new email of user', location='json')
user_edit_parser.add_argument('new_username', nullable=True, required=False, type=str, help='new username of user', location='json')
user_edit_parser.add_argument('new_password', nullable=True, required=False, type=str, help='new password of user', location='json')

@ns.route('/<string:username>')
class UserSearch(Resource):
    @ns.response(code=201, model=user_dto, description='Success')
    @ns.response(code=404, description='Not Found')
    def get(self, username):
        """
        Gets a specified user
        """
        try:
            queried_user = User.query.filter_by(username=username).first()
            if queried_user:
                return marshal(queried_user, user_dto)
            else:
                return {"message": 'user not found'}, 404

        except Exception as e:
            return {"message": str(e)}, 500

    @ns.expect(user_edit_parser)
    def put(self, username):
        """
        Updates an existing user's information
        """
        args = user_edit_parser.parse_args()

        try:
            user_to_be_edited = User.query.filter_by(username=username).first()

            if user_to_be_edited:
                if args['new_email']:
                    user_to_be_edited.email = args['new_email']
                if args['new_username']:
                    user_to_be_edited.username = args['new_username']
                if args['new_password']:
                    user_to_be_edited.password_hash = generate_password_hash(args['new_password'])
            else:
                return {'message': 'user specified not found in database'}, 201

            db.session.commit()
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'user has been edited successfully.'}, 201


user_login_parser = reqparse.RequestParser()
user_login_parser.add_argument('username', required=True, type=str, help='username of user')
user_login_parser.add_argument('password', required=True, type=str, help='password of user')

@ns.route('/login')
class UserLogin(Resource):

    @ns.expect(user_login_parser)
    @ns.response(code=201, model=user_dto, description='Success')
    @ns.response(code=404, description='Not Found')
    def get(self):
        """
        Login a specified user
        """
        args = user_login_parser.parse_args()

        try:
            queried_user = User.query.filter_by(username=args['username']).first()
            if queried_user:
                if check_password_hash(queried_user.password_hash, args['password']):
                    return marshal(queried_user, user_dto)
                else:
                    return {'message': 'invalid password'}, 404
            else:
                return {'message': 'username not found'}, 404

        except Exception as e:
            return {"message": str(e)}, 404





