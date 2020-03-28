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
        response = requests.get('http://user_service:7082/api/users')
        return response.json(), response.status_code

    @ns.expect(user_model, validate=False)
    def post(self):
        """ USERS: Creates a new user """
        response = requests.post('http://user_service:7082/api/users', json=request.json)
        return response.json(), response.status_code


@ns.route('/users/<string:uuid>')
class UserItem(Resource):
    def get(self, uuid):
        """ USERS: Gets a specified user by uuid """
        response = requests.get('http://user_service:7082/api/users/' + uuid)
        return response.json(), response.status_code

    @ns.expect(user_put_model, validate=False)
    def put(self, uuid):
        """ USERS: Updates a user """
        response = requests.put('http://user_service:7082/api/users/' + uuid, json=request.json)
        return response.json(), response.status_code

    def delete(self, uuid):
        """ USERS: Deletes a user """
        response = requests.delete('http://user_service:7082/api/users/' + uuid)
        return response.json(), response.status_code


@ns.route('/users/login')
class UserLogin(Resource):
    @ns.expect(user_model, validate=False)
    def post(self):
        """ USERS: Login for user """
        response = requests.get('http://user_service:7082/api/users/login', params=request.json)
        return response.json(), response.status_code


# Post Service Redirects

@ns.route('/<string:category>/posts')
class PostCollection(Resource):
    def get(self, category):
        """ POSTS: Gets all posts """
        response = requests.get('http://post_service:7082/api/' + category + '/posts')
        return response.json(), response.status_code

    @ns.expect(post_model, validate=False)
    def post(self, category):
        """ POSTS: Creates a new post """
        response = requests.post('http://post_service:7082/api/' + category + '/posts', json=request.json)
        return response.json(), response.status_code


@ns.route('/<string:category>/<string:post_uuid>')
class PostItem(Resource):
    def get(self, category, post_uuid):
        """ POSTS: Gets a specified post by post_uuid """
        response = requests.get('http://post_service:7082/api/' + category + '/' + post_uuid)
        return response.json(), response.status_code

    @ns.expect(post_put_model, validate=False)
    def put(self, category, post_uuid):
        """ POSTS: Updates a post """
        response = requests.put('http://post_service:7082/api/' + category + '/' + post_uuid, json=request.json)
        return response.json(), response.status_code

    def delete(self, category, post_uuid):
        """ POSTS: Deletes a post """
        response = requests.delete('http://post_service:7082/api/' + category + '/' + post_uuid)
        return response.json(), response.status_code


@ns.route('/<string:category>/search/<string:search>')
class PostSearch(Resource):
    def get(self, category, search):
        """ POSTS: Searches for posts """
        response = requests.get('http://post_service:7082/api/' + category + '/search/' + search)
        return response.json(), response.status_code


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
        response = requests.get('http://post_service:7082/api/categories')
        return response.json(), response.status_code

    @ns.expect(category_model)
    def post(self):
        """ CATEGORIES: Creates a new category """
        response = requests.post('http://post_service:7082/api/categories', json=request.json)
        return response.json(), response.status_code


@ns.route('/categories/<string:category>')
class CategoryItem(Resource):
    def get(self, category):
        """ CATEGORIES: Gets a specified category by name """
        response = requests.get('http://post_service:7082/api/categories/' + category)
        return response.json(), response.status_code

    def delete(self, category):
        """ CATEGORIES: Deletes a category """
        response = requests.delete('http://post_service:7082/api/categories/' + category)
        return response.json(), response.status_code


# Comment Service Redirects

@ns.route('/comments')
class CommentsCollection(Resource):
    def get(self):
        """ COMMENTS: Gets all comments """
        response = requests.get('http://comment_service:7082/api/comments')
        return response.json(), response.status_code

    @ns.expect(comment_model)
    def post(self):
        """ COMMENTS: Creates a new comment """
        response = requests.post('http://comment_service:7082/api/comments', json=request.json)
        return response.json(), response.status_code


@ns.route('/comments/<string:comment_uuid>')
class PostItem(Resource):
    @ns.expect(comment_put_model, validate=False)
    def put(self, comment_uuid):
        """ COMMENTS: Updates a comment """
        response = requests.put('http://comment_service:7082/api/comments/' + comment_uuid, json=request.json)
        return response.json(), response.status_code

    def delete(self, comment_uuid):
        """ COMMENTS: Deletes a comment """
        response = requests.delete('http://comment_service:7082/api/comments/' + comment_uuid)
        return response.json(), response.status_code


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