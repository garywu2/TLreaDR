from flask_restplus import reqparse

user_add_parser = reqparse.RequestParser()
user_add_parser.add_argument('email', required=True, type=str, help='email of user', location='json')
user_add_parser.add_argument('username', required=True, type=str, help='username of user', location='json')
user_add_parser.add_argument('password', required=True, type=str, help='password of user', location='json')

user_edit_parser = reqparse.RequestParser()
user_edit_parser.add_argument('new_email', nullable=True, required=False, type=str, help='new email of user', location='json')
user_edit_parser.add_argument('new_username', nullable=True, required=False, type=str, help='new username of user', location='json')
user_edit_parser.add_argument('new_password', nullable=True, required=False, type=str, help='new password of user', location='json')

user_login_parser = reqparse.RequestParser()
user_login_parser.add_argument('username', required=True, type=str, help='username of user')
user_login_parser.add_argument('password', required=True, type=str, help='password of user')