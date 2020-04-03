import requests
from flask import request
from flask_restplus import Resource

from server.models.api_models import *
from server.parsers.server_parsers import *

ns = api.namespace('posts', description='Operations related to post routes', path="/<string:category>")


@ns.route('/posts')
class PostCollection(Resource):
    @ns.expect(post_get_parser)
    def get(self, category):
        """ Gets all posts """
        try:
            response = requests.get('http://post_service:7082/api/' + category + '/posts',
                                    params=post_get_parser.parse_args())
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError as c:
            return {"message": "post service is unavailable"}, 503

    @ns.expect(post_model, validate=False)
    def post(self, category):
        """ Creates a new post """
        response = requests.post('http://post_service:7082/api/' + category + '/posts', json=request.json)
        return response.json(), response.status_code


@ns.route('/<string:post_uuid>')
class PostItem(Resource):
    @ns.expect(post_get_parser)
    def get(self, category, post_uuid):
        """ Gets a specified post by post_uuid """
        try:
            response = requests.get('http://post_service:7082/api/' + category + '/' + post_uuid,
                                    params=post_get_parser.parse_args())
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError as c:
            return {"message": "post service is unavailable"}, 503

    @ns.expect(post_put_model, validate=False)
    def put(self, category, post_uuid):
        """ Updates a post """
        response = requests.put('http://post_service:7082/api/' + category + '/' + post_uuid, json=request.json)
        return response.json(), response.status_code

    def delete(self, category, post_uuid):
        """ Deletes a post """
        response = requests.delete('http://post_service:7082/api/' + category + '/' + post_uuid)
        return response.json(), response.status_code


@ns.route('/search/<string:search>')
class PostSearch(Resource):
    @ns.expect(post_get_parser)
    def get(self, category, search):
        """ Searches for posts """
        try:
            response = requests.get('http://post_service:7082/api/' + category + '/search/' + search,
                                params=post_get_parser.parse_args())
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError as c:
            return {"message": "post service is unavailable"}, 503

@ns.route('/posts/<string:user_uuid>')
class UserPosts(Resource):
    def get(self, category, user_uuid):
        """ Gets all posts by user """
        try:
            response = requests.get('http://post_service:7082/api/' + category + '/posts/' + user_uuid)
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError as c:
            return {"message": "post service is unavailable"}, 503

@ns.route('/<string:post_uuid>/vote')
class PostVote(Resource):
    @ns.expect(vote_post_model)
    def post(self, category, post_uuid):
        """ Creates a vote on a post """
        response = requests.post('http://post_service:7082/api/' + category + '/' + post_uuid + '/vote',
                                 json=request.json)
        return response.json(), response.status_code

    @ns.expect(vote_put_model)
    def put(self, category, post_uuid):
        """ Updates a vote on a post """
        response = requests.put('http://post_service:7082/api/' + category + '/' + post_uuid + '/vote',
                                json=request.json)
        return response.json(), response.status_code

    @ns.expect(vote_delete_model)
    def delete(self, category, post_uuid):
        """ Deletes a vote on a post """
        response = requests.delete('http://post_service:7082/api/' + category + '/' + post_uuid + '/vote',
                                   json=request.json)
        return response.json(), response.status_code
