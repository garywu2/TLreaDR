from datetime import datetime

import requests
from flask_restplus import Resource, fields, marshal

import post_service.managers.post_manager as post_manager
from post_service.api.restplus import api
from post_service.models import db
from post_service.models.category import Category
from post_service.models.post import Post
from post_service.models.postvote import Postvote
from post_service.parsers.post_parsers import *

ns = api.namespace('posts', description='Operations related to posts', path="/<string:category>")

post_dto = api.model('post', {
    'post_uuid': fields.String(required=True, description='post uuid'),
    'title': fields.String(required=True, description='title of the post'),
    'body': fields.String(required=True, description='body of the post'),
    'pub_date': fields.String(required=True, description='published date'),
    'edited_date': fields.String(description='published date'),
    'image_link': fields.String(description='image link of the post'),
    'article_link': fields.String(description='article link of the post'),
    'votes': fields.Integer(required=True, descrption='votes of the post'),
    'category_uuid': fields.String(required=True, description='category uuid'),
    'category': fields.String(required=True, description='category of the post'),
    'author_uuid': fields.String(required=True, description='uuid of author'),
    'author_username': fields.String(required=True, description='username of author'),
    'new_flag': fields.Boolean(required=True, description='new flag for the post'),
    'edited_flag': fields.Boolean(required=True, description='new flag for the post'),
    'vote_type': fields.Integer(required=False, description='status of user vote')
})


@ns.route('/posts')
class PostCollection(Resource):
    @ns.response(code=200, description='Success')
    @ns.response(code=404, description='Not Found')
    @ns.expect(post_get_parser)
    def get(self, category):
        """
        Gets all uploaded posts
        """
        args = post_get_parser.parse_args()
        try:
            if category != 'all' and Category.query.filter_by(name=category).first() is None:
                return {"message": "category not found."}, 404

            posts = post_manager.get_posts_by_category(category, args['user_uuid'])
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
                            args['image_link'], args['article_link'])
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
        result_post = post_manager.get_post_by_post_uuid(post_uuid, args['user_uuid'])
        return result_post, 200

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
                if args['new_article_link']:
                    post_to_be_edited.article_link = args['new_article_link']

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

            response = requests.delete('http://comment_service:7082/api/comments/post/' + str(post_uuid))
            if response.status_code != 200:
                return {'message': 'error deleting posts comments'}, response.status_code

            if post_to_be_deleted:
                db.session.delete(post_to_be_deleted)
                db.session.commit()
            else:
                return {'message': 'post not found.'}, 404
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'post has been deleted successfully.'}, 200


@ns.route('/search/<string:search>')
class PostSearch(Resource):
    @ns.marshal_list_with(post_dto, envelope='posts')
    @ns.expect(post_get_parser)
    def get(self, category, search):
        """
        Searches for posts given a string query
        """
        args = post_get_parser.parse_args()

        posts = post_manager.get_posts_by_category(category, args['user_uuid'])
        result_posts = []
        for post in posts:
            if search in post.title or search in post.body:
                result_posts.append(post)

        return result_posts


@ns.route('/posts/<string:user_uuid>')
class UserPosts(Resource):
    @ns.marshal_list_with(post_dto, envelope='posts')
    def get(self, category, user_uuid):
        """
        Returns posts of the specified user
        """
        result_posts = post_manager.get_posts_by_user_uuid(user_uuid)
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

            post_voted_on.assign_vote(args['vote_type'])

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
                post_to_be_edited.assign_vote(2 * new_vote_type)
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
