from flask_restplus import reqparse

post_get_parser = reqparse.RequestParser()
post_get_parser.add_argument('user_uuid', required=False, type=str, help='user that requested get')

post_add_parser = reqparse.RequestParser()
post_add_parser.add_argument('title', required=True, type=str, help='title of post', location='json')
post_add_parser.add_argument('body', required=True, type=str, help='body of post', location='json')
post_add_parser.add_argument('image_link', type=str, help='link of attached image', location='json')
post_add_parser.add_argument('article_link', type=str, help='link of attached image', location='json')
post_add_parser.add_argument('author_uuid', type=str, required=True, help='author uuid', location='json')

post_edit_parser = reqparse.RequestParser()
post_edit_parser.add_argument('new_title', nullable=True, type=str, help='new title of post', location='json')
post_edit_parser.add_argument('new_body', nullable=True, type=str, help='new body of post', location='json')
post_edit_parser.add_argument('new_image_link', nullable=True, type=str, help='new image link', location='json')
post_edit_parser.add_argument('new_article_link', nullable=True, type=str, help='new image link', location='json')

post_vote_add_parser = reqparse.RequestParser()
post_vote_add_parser.add_argument('user_uuid', required=True, type=str, help='uuid of user', location='json')
post_vote_add_parser.add_argument('vote_type', required=True, type=int, help='vote type', location='json')

post_vote_edit_parser = reqparse.RequestParser()
post_vote_edit_parser.add_argument('user_uuid', required=True, type=str, help='uuid of user', location='json')
post_vote_edit_parser.add_argument('new_vote_type', required=True, type=int, help='vote type', location='json')

post_vote_delete_parser = reqparse.RequestParser()
post_vote_delete_parser.add_argument('user_uuid', required=True, type=str, help='uuid of user', location='json')