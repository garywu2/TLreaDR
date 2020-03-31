from flask_restplus import reqparse

post_get_parser = reqparse.RequestParser()
post_get_parser.add_argument('user_uuid', required=False, type=str, help='user that requested get')

user_login_parser = reqparse.RequestParser()
user_login_parser.add_argument('username', required=True, type=str, help='username of user logging in')
user_login_parser.add_argument('password', required=True, type=str, help='password of user logging in')
