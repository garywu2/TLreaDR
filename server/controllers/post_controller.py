from flask_restplus import Resource, fields, reqparse, marshal

from server.api.restplus import api
from server.models import db
from server.models.post import Post

ns = api.namespace('posts', description='Operations related to posts')

post_dto = api.model('post', {
    'post_uuid': fields.String(required=True, description='post uuid'),
    'title': fields.String(required=True, description='title of the post'),
    'body': fields.String(required=True, description='body of the post'),
    'pub_date': fields.String(required=True, description='published date'),
    'image_link': fields.String(description='image link of the post'),
    'category_uuid': fields.String(required=True, description='category uuid'),
    'category': fields.String(required=True, description='category of the post'),
    'author_uuid': fields.String(required=True, description='author uuid')
})

post_add_parser = reqparse.RequestParser()
post_add_parser.add_argument('title', required=True, type=str, help='title of post', location='json')
post_add_parser.add_argument('body', required=True, type=str, help='body of post', location='json')
post_add_parser.add_argument('image_link', type=str, help='link of attached image', location='json')
post_add_parser.add_argument('category_uuid', type=str, required=True, help='category uuid', location='json')
post_add_parser.add_argument('author_uuid', type=str, required=True, help='author uuid', location='json')

@ns.route('/')
class PostCollection(Resource):
    @api.expect(post_add_parser)
    def post(self):
        """
        Create a new posts
        """
        args = post_add_parser.parse_args()

        try:
            new_post = Post(args['title'], args['body'], args['category_uuid'], args['author_uuid'], args['image_link'])
            db.session.add(new_post)
            db.session.commit()
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'post has been created successfully.'}, 201