from flask_restplus import reqparse

post_get_parser = reqparse.RequestParser()
post_get_parser.add_argument('user_uuid', required=False, type=str, help='user that requested get')
