from flask_restplus import reqparse

comment_parser = reqparse.RequestParser()
comment_parser.add_argument('text', required=True, type=str, help='comment text', location='json')
comment_parser.add_argument('author_uuid', required=True, type=str, help='comment author uuid', location='json')
comment_parser.add_argument('post_uuid', required=True, type=str, help='comment post uuid', location='json')
comment_parser.add_argument('parent_id', type=str, help='comment parent id', location='json')

comment_edit_parser = reqparse.RequestParser()
comment_edit_parser.add_argument('new_text', required=True, type=str, help='new title of post', location='json')