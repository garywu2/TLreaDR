from datetime import datetime, timedelta

import requests
from flask_restplus import Resource, fields, reqparse, marshal
from sqlalchemy import desc

from post_service.api.restplus import api
from post_service.models import db
from post_service.models.category import Category
from post_service.models.post import Post

ns = api.namespace('posts', description='Operations related to posts', path="/<string:category>")

user_dto = api.model('user', {
    'user_uuid': fields.String(required=True, description='user uuid'),
    'email': fields.String(required=True, description='user email address'),
    'username': fields.String(required=True, description='user username'),
})

post_dto = api.model('post', {
    'post_uuid': fields.String(required=True, description='post uuid'),
    'title': fields.String(required=True, description='title of the post'),
    'body': fields.String(required=True, description='body of the post'),
    'pub_date': fields.String(required=True, description='published date'),
    'edited_date': fields.String(description='published date'),
    'image_link': fields.String(description='image link of the post'),
    'upvotes': fields.Integer(required=True, descrption='upvotes of the post'),
    'downvotes': fields.Integer(required=True, descrption='downvotes of the post'),
    'category_uuid': fields.String(required=True, description='category uuid'),
    'category': fields.String(required=True, description='category of the post'),
    'author': fields.Nested(user_dto),
    'new_flag': fields.Boolean(required=True, description='new flag for the post'),
    'edited_flag': fields.Boolean(required=True, description='new flag for the post')
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


def get_author(author_uuid):
    return requests.get('http://user_service:7082/api/users/' + str(author_uuid)).json()


# Nests author information inside the post json
def nest_author_info(post):
    user = get_author(post.author_uuid)
    post.author = marshal(user, user_dto)

    return post


def get_all_posts():
    # Calculates 3 days prior to current time
    three_days_ago = datetime.utcnow() - timedelta(days=3)
    # Obtains posts from recent 3 days (new posts)
    new_ordered_posts = Post.query \
        .filter(Post.pub_date > three_days_ago) \
        .order_by(desc(Post.upvotes - Post.downvotes)).all()
    # Obtains posts from prior to recent 3 days (old posts)
    not_new_ordered_posts = Post.query \
        .filter(Post.pub_date <= three_days_ago) \
        .order_by(desc(Post.upvotes - Post.downvotes)).all()

    # Appends the old posts to the new posts
    result_posts = new_ordered_posts
    for post in not_new_ordered_posts:
        if post is not None:
            # Inverts new post flag to false as post was queried in old posts
            post.invert_new_flag()
            result_posts.append(post)

    for post in result_posts:
        nest_author_info(post)

    return result_posts


def get_posts_by_category(category):
    if category == "all":
        return get_all_posts()

    queried_category = Category.query.filter_by(name=category).first()
    # Calculates 3 days prior to current time
    three_days_ago = datetime.utcnow() - timedelta(days=3)
    # Obtains posts from recent 3 days with category filter (new posts)
    new_ordered_posts = Post.query \
        .filter_by(category_uuid=queried_category.category_uuid) \
        .filter(Post.pub_date > three_days_ago) \
        .order_by(desc(Post.upvotes - Post.downvotes)).all()
    # Obtains posts from prior to recent 3 days with category filter (old posts)
    not_new_ordered_posts = Post.query \
        .filter_by(category_uuid=queried_category.category_uuid) \
        .filter(Post.pub_date <= three_days_ago) \
        .order_by(desc(Post.upvotes - Post.downvotes)).all()

    # Appends the old posts to the new posts
    result_posts = new_ordered_posts
    for post in not_new_ordered_posts:
        if post is not None:
            post.invert_new_flag()
            result_posts.append(post)

    for post in result_posts:
        nest_author_info(post)

    return result_posts


@ns.route('/posts')
class PostCollection(Resource):
    @ns.response(code=201, model=user_dto, description='Success')
    @ns.response(code=404, description='Not Found')
    def get(self, category):
        """
        Gets all uploaded posts
        """
        try:
            if category is None:
                return {"message": "category not found."}, 201

            return marshal(get_posts_by_category(category), post_dto, envelope='posts'), 200
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
            return {"message": "category not found."}, 201

        try:
            new_post = Post(args['title'], args['body'], queried_category.category_uuid, args['author_uuid'],
                            args['image_link'])
            db.session.add(new_post)
            db.session.commit()
        except Exception as e:
            return {"message": str(e)}, 500

        return marshal(new_post, post_dto), 200


@ns.route('/<string:post_uuid>')
class PostItem(Resource):
    @ns.marshal_list_with(post_dto)
    def get(self, post_uuid, category):
        """
        Gets a post given its UUID
        """
        result_post = Post.query.filter_by(post_uuid=post_uuid).first()
        nest_author_info(result_post)
        return result_post

    @ns.expect(post_edit_parser)
    def put(self, post_uuid, category):
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


@ns.route('/search/<string:search>')
class PostSearch(Resource):
    @ns.marshal_list_with(post_dto, envelope='posts')
    def get(self, category, search):
        posts = get_posts_by_category(category)
        result_posts = []
        for post in posts:
            if search in post.title or search in post.body:
                result_posts.append(post)

        return result_posts


@ns.route('/posts/<string:user_uuid>')
class UserPosts(Resource):
    @ns.marshal_list_with(post_dto, envelope='posts')
    def get(self, category, user_uuid):
        result_posts = Post.query.filter_by(author_uuid=user_uuid) \
                            .order_by(desc(Post.pub_date)).all()

        for post in result_posts:
            nest_author_info(post)

        return result_posts