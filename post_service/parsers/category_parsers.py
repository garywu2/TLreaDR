from flask_restplus import reqparse

category_parser = reqparse.RequestParser()
category_parser.add_argument('name', required=True, type=str, help='name of category', location='json')