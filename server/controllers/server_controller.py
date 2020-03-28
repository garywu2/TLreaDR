import requests
from flask import request
from flask_restplus import Resource

from server.models.expected_models import *

ns = api.namespace('api', description='Operations related to server routes')


# User Service Redirects

@ns.route('/users')
class UserCollection(Resource):
    def get(self):
        """ USERS: Gets all users """
        return requests.get('http://user_service:7082/api/users').json()

    @ns.expect(user_model, validate=False)
    def post(self):
        """ USERS: Creates a new user """
        return requests.post('http://user_service:7082/api/users', json=request.json).json()


@ns.route('/users/<string:uuid>')
class UserItem(Resource):
    def get(self, uuid):
        """ USERS: Gets a specified user by uuid """
        return requests.get('http://user_service:7082/api/users/' + uuid).json()

    @ns.expect(user_put_model, validate=False)
    def put(self, uuid):
        """ USERS: Updates a user """
        return requests.put('http://user_service:7082/api/users/' + uuid, json=request.json).json()

    def delete(self, uuid):
        """ USERS: Deletes a user """
        return requests.delete('http://user_service:7082/api/users/' + uuid).json()


@ns.route('/users/login')
class UserLogin(Resource):
    @ns.expect(user_model, validate=False)
    def post(self):
        """ USERS: Login for user """
        return requests.get('http://user_service:7082/api/users/login', params=request.json).json()


# Post Service Redirects

@ns.route('/<string:category>/posts')
class PostCollection(Resource):
    def get(self, category):
        """ POSTS: Gets all posts """
        return requests.get('http://post_service:7082/api/' + category + '/posts').json()

    @ns.expect(post_model, validate=False)
    def post(self, category):
        """ POSTS: Creates a new post """
        return requests.post('http://post_service:7082/api/' + category + '/posts', json=request.json).json()


@ns.route('/<string:category>/<string:post_uuid>')
class PostItem(Resource):
    def get(self, category, post_uuid):
        """ POSTS: Gets a specified post by post_uuid """
        return requests.get('http://post_service:7082/api/' + category + '/' + post_uuid).json()

    @ns.expect(post_put_model, validate=False)
    def put(self, category, post_uuid):
        """ POSTS: Updates a post """
        return requests.put('http://post_service:7082/api/' + category + '/' + post_uuid, json=request.json).json()

    def delete(self, category, post_uuid):
        """ POSTS: Deletes a post """
        return requests.delete('http://post_service:7082/api/' + category + '/' + post_uuid).json()


@ns.route('/<string:category>/search/<string:search>')
class PostSearch(Resource):
    def get(self, category, search):
        """ POSTS: Searches for posts """
        return requests.get('http://post_service:7082/api/' + category + '/search/' + search).json()


@ns.route('/<string:category>/posts/<string:user_uuid>')
class UserPosts(Resource):
    def get(self, category, user_uuid):
        """ POSTS: Gets all posts by user """
        return requests.get('http://post_service:7082/api/' + category + '/posts/' + user_uuid).json()


# Category (Post Service) Redirects

@ns.route('/categories')
class CategoryCollection(Resource):
    def get(self):
        """ CATEGORIES: Gets all categories """
        return requests.get('http://post_service:7082/api/categories').json()

    @ns.expect(category_model)
    def post(self):
        """ CATEGORIES: Creates a new category """
        return requests.post('http://post_service:7082/api/categories', json=request.json).json()


@ns.route('/categories/<string:category>')
class CategoryItem(Resource):
    def get(self, category):
        """ CATEGORIES: Gets a specified category by name """
        return requests.get('http://post_service:7082/api/categories/' + category).json()

    def delete(self, category):
        """ CATEGORIES: Deletes a category """
        return requests.delete('http://post_service:7082/api/categories/' + category).json()


# Comment Service Redirects

@ns.route('/comments')
class CommentsCollection(Resource):
    def get(self):
        """ COMMENTS: Gets all comments """
        return requests.get('http://comment_service:7082/api/comments').json()

    @ns.expect(comment_model)
    def post(self):
        """ COMMENTS: Creates a new comment """
        return requests.post('http://comment_service:7082/api/comments', json=request.json).json()


@ns.route('/comments/<string:comment_uuid>')
class PostItem(Resource):
    @ns.expect(comment_put_model, validate=False)
    def put(self, comment_uuid):
        """ COMMENTS: Updates a comment """
        return requests.put('http://comment_service:7082/api/comments/' + comment_uuid, json=request.json).json()

    def delete(self, comment_uuid):
        """ COMMENTS: Deletes a comment """
        return requests.delete('http://comment_service:7082/api/comments/' + comment_uuid).json()


@ns.route('/comments/post/<string:post_uuid>')
class PostComment(Resource):
    def get(self, post_uuid):
        """ COMMENTS: Gets all comments for a post """
        return requests.get('http://comment_service:7082/api/comments/post/' + post_uuid).json()


@ns.route('/comments/user/<string:user_uuid>')
class UserComments(Resource):
    def get(self, user_uuid):
        """ COMMENTS: Gets all comments for a user """
        return requests.get('http://comment_service:7082/api/comments/user/' + user_uuid).json()
