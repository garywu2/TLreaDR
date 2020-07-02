from flask_restplus import Resource, marshal

import post_service.managers.post_manager as post_manager
from post_service.api.models import post_dto
from post_service.api.restplus import api
from post_service.models.category import Category
from post_service.parsers.post_parsers import *

ns = api.namespace('posts', description='Operations related to posts', path="/<string:category>")


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
        try:
            new_post = post_manager.add_post(category, args)
            return new_post
        except Exception as e:
            return {"message": str(e)}, 500


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
            post_manager.edit_post(post_uuid, args)
            return {'message': 'post has been edited successfully.'}, 200
        except Exception as e:
            return {"message": str(e)}, 500

    def delete(self, post_uuid, category):
        """
        Deletes a post
        """
        try:
            message = post_manager.delete_post(post_uuid)
            return message
        except Exception as e:
            return {"message": str(e)}, 500


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
        result_posts = [p for p in posts if search in p.title or search in p.body]
        return result_posts, 200


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
            post_manager.add_post_vote(post_uuid, args)
            return {'message': 'vote has been created successfully.'}, 201
        except Exception as e:
            return {"message": str(e)}, 500

    @ns.expect(post_vote_edit_parser)
    def put(self, post_uuid, category):
        """
        Updates a vote record
        """
        args = post_vote_edit_parser.parse_args()
        try:
            message = post_manager.edit_post_vote(post_uuid, args)
            return message
        except Exception as e:
            return {"message": str(e)}, 500

    @ns.expect(post_vote_delete_parser)
    def delete(self, post_uuid, category):
        """
        Deletes a vote
        """
        args = post_vote_delete_parser.parse_args()
        try:
            post_manager.delete_post_vote(post_uuid, args)
            return {'message': 'vote has been deleted successfully.'}, 201
        except Exception as e:
            return {"message": str(e)}, 500

@ns.route('/summarize')
class PostSummary(Resource):
    @ns.expect(article_summarize_parser)
    def get(self, category):
        """
        Summarizes an article
        """
        args = article_summarize_parser.parse_args()
        return post_manager.get_summary(args['article_link'])