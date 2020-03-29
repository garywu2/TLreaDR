from datetime import datetime, timedelta

import requests
from flask_restplus import Resource, fields, marshal
from sqlalchemy import desc

from post_service.api.restplus import api
from post_service.models import db
from post_service.models.category import Category
from post_service.models.post import Post
from post_service.models.postvote import Postvote
from post_service.parsers.post_parsers import *

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
    'edited_flag': fields.Boolean(required=True, description='new flag for the post'),
    'vote_type': fields.Integer(required=False, description='status of user vote')
})


def get_author(author_uuid):
    return requests.get('http://user_service:7082/api/users/' + str(author_uuid)).json()


# Nests author information inside the post json
def nest_author_info(post):
    user = get_author(post.author_uuid)
    post.author = marshal(user, user_dto)

    return post


def get_posts_by_category(category, user_uuid):
    post_query = Post.query

    if category != 'all':
        queried_category = Category.query.filter_by(name=category).first()
        post_query = post_query.filter_by(category_uuid=queried_category.category_uuid)

    filteredPostVote = Postvote.query.filter_by(user_uuid=user_uuid).subquery()
    # Calculates 3 days prior to current time
    three_days_ago = datetime.utcnow() - timedelta(days=3)
    # Obtains posts from recent 3 days with category filter (new posts)
    new_ordered_posts = post_query.filter(Post.pub_date > three_days_ago) \
        .order_by(desc(Post.upvotes - Post.downvotes), desc(Post.pub_date))

    # Obtains posts from prior to recent 3 days with category filter (old posts)
    not_new_ordered_posts = post_query.filter(Post.pub_date <= three_days_ago) \
        .order_by(desc(Post.upvotes - Post.downvotes), desc(Post.pub_date))

    # Appends the old posts to the new posts
    result_posts = new_ordered_posts.all()
    for post in not_new_ordered_posts.all():
        result_posts.append(post)
        if post is not None:
            post.invert_new_flag()

    for post in result_posts:
        nest_author_info(post)
        get_post_vote(post, user_uuid)

    return result_posts


def get_post_vote(post, user_uuid):
    vote = Postvote.query.filter_by(post_uuid=post.post_uuid) \
        .filter_by(user_uuid=user_uuid).first()
    if vote:
        post.vote_type = vote.vote_type
    else:
        post.vote_type = None


@ns.route('/posts')
class PostCollection(Resource):
    @ns.response(code=201, model=user_dto, description='Success')
    @ns.response(code=404, description='Not Found')
    @ns.expect(post_get_parser)
    def get(self, category):
        """
        Gets all uploaded posts
        """
        args = post_get_parser.parse_args()
        try:
            if not Category.query.filter_by(name=category).first():
                return {"message": "category not found."}, 404

            posts = get_posts_by_category(category, args['user_uuid'])
            return marshal(posts, post_dto, envelope='posts'), 200
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
    @ns.expect(post_get_parser)
    def get(self, post_uuid, category):
        """
        Gets a post given its UUID
        """
        args = post_get_parser.parse_args()

        result_post = Post.query.filter_by(post_uuid=post_uuid).first()
        nest_author_info(result_post)
        if args['user_uuid']:
            get_post_vote(result_post, args['user_uuid'])
        else:
            result_post.user_requested_vote = None

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
                return {'message': 'post specified not found in database'}, 404

            db.session.commit()
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'post has been edited successfully.'}, 200

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
    @ns.expect(post_get_parser)
    def get(self, category, search):
        """
        Searches for posts given a string query
        """
        args = post_get_parser.parse_args()

        posts = get_posts_by_category(category)
        result_posts = []
        for post in posts:
            if search in post.title or search in post.body:
                result_posts.append(post)

        for post in result_posts:
            if args['user_uuid']:
                get_post_vote(post, args['user_uuid'])
            else:
                post.user_requested_vote = None

        return result_posts


@ns.route('/posts/<string:user_uuid>')
class UserPosts(Resource):
    @ns.marshal_list_with(post_dto, envelope='posts')
    @ns.expect(post_get_parser)
    def get(self, category, user_uuid):
        """
        Returns posts of the specified user
        """
        args = post_get_parser.parse_args()

        result_posts = Post.query.filter_by(author_uuid=user_uuid) \
            .order_by(desc(Post.pub_date)).all()

        for post in result_posts:
            nest_author_info(post)
            if args['user_uuid']:
                get_post_vote(post, args['user_uuid'])
            else:
                post.user_requested_vote = None

        return result_posts


@ns.route('/<string:post_uuid>/vote')
class PostVote(Resource):
    @ns.expect(post_vote_add_parser)
    def post(self, category, post_uuid):
        """
        Creates a vote record
        """
        args = post_vote_add_parser.parse_args()

        try:
            new_post_vote = Postvote(post_uuid, args['user_uuid'], args['vote_type'])
            post_voted_on = Post.query.filter_by(post_uuid=post_uuid).first()

            post_voted_on.assign_vote(args['vote_type'], False)

            db.session.add(new_post_vote)
            db.session.commit()

        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'vote has been created successfully.'}, 201

    @ns.expect(post_vote_edit_parser)
    def put(self, post_uuid, category):
        """
        Updates a vote record
        """
        args = post_vote_edit_parser.parse_args()

        try:
            user_uuid = args['user_uuid']
            new_vote_type = args['new_vote_type']
            post_to_be_edited = Post.query.filter_by(post_uuid=post_uuid).first()
            vote_to_be_edited = Postvote.query.filter_by(post_uuid=post_uuid) \
                .filter_by(user_uuid=user_uuid).first()

            if vote_to_be_edited and post_to_be_edited:
                if vote_to_be_edited.vote_type == new_vote_type:
                    return {'message': 'cannot vote twice on the same post'}, 404
                vote_to_be_edited.vote_type = new_vote_type
                post_to_be_edited.assign_vote(new_vote_type, True)
            else:
                return {'message': 'vote or post not found.'}, 404

            db.session.commit()

            return {'message': 'vote has been edited successfully.'}, 201

        except Exception as e:
            return {"message": str(e)}, 500

    @ns.expect(post_vote_delete_parser)
    def delete(self, post_uuid, category):
        """
        Deletes a vote
        """
        args = post_vote_delete_parser.parse_args()

        try:
            user_uuid = args['user_uuid']
            post_to_be_edited = Post.query.filter_by(post_uuid=post_uuid).first()
            vote_to_be_deleted = Postvote.query.filter_by(post_uuid=post_uuid) \
                .filter_by(user_uuid=user_uuid).first()

            post_to_be_edited.delete_vote(vote_to_be_deleted.vote_type)

            db.session.delete(vote_to_be_deleted)
            db.session.commit()

        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'vote has been deleted successfully.'}, 201
