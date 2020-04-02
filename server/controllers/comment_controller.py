import requests
from flask import request
from flask_restplus import Resource

from server.models.api_models import *

ns = api.namespace('comments', description='Operations related to server routes')


@ns.route('')
class CommentsCollection(Resource):
    def get(self):
        """ Gets all comments """
        response = requests.get('http://comment_service:7082/api/comments')
        return response.json(), response.status_code

    @ns.expect(comment_model)
    def post(self):
        """ Creates a new comment """
        response = requests.post('http://comment_service:7082/api/comments', json=request.json)
        return response.json(), response.status_code


@ns.route('/<string:comment_uuid>')
class PostItem(Resource):
    @ns.expect(comment_put_model, validate=False)
    def put(self, comment_uuid):
        """ Updates a comment """
        response = requests.put('http://comment_service:7082/api/comments/' + comment_uuid, json=request.json)
        return response.json(), response.status_code

    def delete(self, comment_uuid):
        """ Deletes a comment """
        response = requests.delete('http://comment_service:7082/api/comments/' + comment_uuid)
        return response.json(), response.status_code


@ns.route('/<string:post_uuid>')
class PostComment(Resource):
    def get(self, post_uuid):
        """ Gets all comments for a post """
        response = requests.get('http://comment_service:7082/api/comments/post/' + post_uuid)
        return response.json(), response.status_code

    def delete(self, post_uuid):
        """ Deletes all comments for a post """
        response = requests.delete('http://comment_service:7082/api/comments/post/' + post_uuid)
        return response.json(), response.status_code


@ns.route('/user/<string:user_uuid>')
class UserComments(Resource):
    def get(self, user_uuid):
        """ Gets all comments for a user """
        response = requests.get('http://comment_service:7082/api/comments/user/' + user_uuid)
        return response.json(), response.status_code
