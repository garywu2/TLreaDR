from datetime import datetime

from flask_restplus import Resource, fields, reqparse, marshal

from post_service.api.restplus import api
# from post_service.controllers.user_controller import user_dto
from post_service.models import db
# from post_service.models.category import Category
from post_service.models.post import Post
# from post_service.models.user import User

ns = api.namespace('posts', description='Operations related to posts', path="/<string:category>")

# TODO This post controller has ALOT of dependency on the Users table which should be changed after implementing microservices

post_dto = api.model('post', {
    'post_uuid': fields.String(required=True, description='post uuid'),
    'title': fields.String(required=True, description='title of the post'),
    'body': fields.String(required=True, description='body of the post'),
    'pub_date': fields.String(required=True, description='published date'),
    'image_link': fields.String(description='image link of the post'),
    'category_uuid': fields.String(required=True, description='category uuid'),
    'category': fields.String(required=True, description='category of the post'),
    # 'author': fields.Nested(user_dto)
})

post_add_parser = reqparse.RequestParser()
post_add_parser.add_argument('title', required=True, type=str, help='title of post', location='json')
post_add_parser.add_argument('body', required=True, type=str, help='body of post', location='json')
post_add_parser.add_argument('image_link', type=str, help='link of attached image', location='json')
post_add_parser.add_argument('author_uuid', type=str, required=True, help='author uuid', location='json')

post_edit_parser = reqparse.RequestParser()
post_edit_parser.add_argument('new_title', nullable=True, type=str, help='new title of post', location='json')
post_edit_parser.add_argument('new_body', nullable=True, type=str, help='new body of post', location='json')
post_edit_parser.add_argument('new_image_link', nullable=True, type=str, help='new image link', location='json')


# def get_author(author_uuid):
#     return User.query.filter_by(user_uuid=author_uuid).first()
#
#
# @ns.route('/posts')
# class PostCollection(Resource):
#     @ns.marshal_list_with(post_dto, envelope='posts')
#     def get(self, category):
#         """
#         Gets all uploaded posts
#         """
#         if category == "all":
#             posts = Post.query.all()
#             for post in posts:
#                 user = get_author(post.author_uuid)
#                 post.author = marshal(user, user_dto)
#         else:
#             try:
#                 queried_category = Category.query.filter_by(name=category).first()
#
#                 if queried_category is None:
#                     return {"message": "category not found."}, 201
#
#                 posts = Post.query.filter_by(category_uuid=queried_category.category_uuid).all()
#                 for post in posts:
#                     user = get_author(post.author_uuid)
#                     post.author = marshal(user, user_dto)
#             except Exception as e:
#                 return {"message": str(e)}, 500
#
#         return posts, 200
#
#     @api.expect(post_add_parser)
#     def post(self, category):
#         """
#         Create a new posts
#         """
#         args = post_add_parser.parse_args()
#
#         queried_category = Category.query.filter_by(name=category).first()
#
#         if queried_category is None:
#             return {"message": "category not found."}, 201
#
#         try:
#             new_post = Post(args['title'], args['body'], queried_category.category_uuid, args['author_uuid'],
#                             args['image_link'])
#             db.session.add(new_post)
#             db.session.commit()
#         except Exception as e:
#             return {"message": str(e)}, 500
#
#         return {'message': 'post has been created successfully.'}, 201


@ns.route('/<string:post_uuid>')
class PostItem(Resource):
    @ns.expect(post_edit_parser)
    def put(self, category, post_uuid):
        """
        Updates an existing post's information
        """
        args = post_edit_parser.parse_args()

        try:
            post_to_be_edited = Post.query.filter_by(post_uuid=post_uuid).first()

            if post_to_be_edited:
                if args['new_title']:
                    post_to_be_edited.title = args['new_title']
                if args['new_body']:
                    post_to_be_edited.body = args['new_body']
                if args['new_image_link']:
                    post_to_be_edited.image_link = args['new_image_link']

                post_to_be_edited.edited_date = datetime.utcnow()
                post_to_be_edited.edited_flag = True
            else:
                return {'message': 'post specified not found in database'}, 201

            db.session.commit()
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'post has been edited successfully.'}, 201

    def delete(self, post_uuid, category):
        """
        Deletes a post
        """

        try:
            post_to_be_deleted = Post.query.filter_by(post_uuid=post_uuid).first()
            if post_to_be_deleted:
                db.session.delete(post_to_be_deleted)
                db.session.commit()
            else:
                return {'message': 'post not found.'}, 404
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'post has been deleted successfully.'}, 201
