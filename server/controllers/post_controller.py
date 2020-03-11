from flask_restplus import Resource, fields, reqparse, marshal

from server.api.restplus import api
from server.models import db
from server.models.post import Post
from server.models.category import Category

ns = api.namespace('posts', description='Operations related to posts', path="/<string:category>")

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
post_add_parser.add_argument('author_uuid', type=str, required=True, help='author uuid', location='json')


@ns.route('/posts')
class PostCollection(Resource):
    @ns.marshal_list_with(post_dto)
    def get(self, category):
        """
        Gets all uploaded posts
        """
        if category=="all":
            results = Post.query.all()
            return results
        
        try:
            queried_category = Category.query.filter_by(name=category).first()

            if queried_category is None:
                return{"message": "category not found."}, 201

            results = Post.query.filter_by(category_uuid=queried_category.category_uuid).all()
            return results
        except Exception as e:
            return {"message": str(e)}, 500

    @api.expect(post_add_parser)
    def post(self, category):
        """
        Create a new posts
        """
        args = post_add_parser.parse_args()

        queried_category = Category.query.filter_by(name=category).first()

        if queried_category is None:
            return{"message": "category not found."}, 201

        try:
            new_post = Post(args['title'], args['body'], queried_category.category_uuid, args['author_uuid'], args['image_link'])
            db.session.add(new_post)
            db.session.commit()
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'post has been created successfully.'}, 201