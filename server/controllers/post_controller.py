import requests
from flask import request
from flask_restplus import Resource

import datetime
from server.models.event import db
from server.models.event import Event

from server.models.api_models import *
from server.parsers.server_parsers import *

ns = api.namespace('posts', description='Operations related to post routes', path="/<string:category>")


@ns.route('/posts')
class PostCollection(Resource):
    @ns.expect(post_get_parser)
    def get(self, category):
        """ Gets all posts """
        response = requests.get('http://post_service:7082/api/' + category + '/posts',
                                params=post_get_parser.parse_args())
        return response.json(), response.status_code

    @ns.expect(post_model, validate=False)
    def post(self, category):
        """ Creates a new post """
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "add"
        request.json["type"] = "post"
        request.json["category"] = category
        deleted_post_event = Event(request.json)
        try:
            db.session.add(deleted_post_event)
            db.session.commit()
            #response = requests.post('http://post_service:7082/api/' + category + '/posts', json=request.json)
            #return response.json(), response.status_code
            return "New Post Event Created", 200

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500


@ns.route('/<string:post_uuid>')
class PostItem(Resource):
    @ns.expect(post_get_parser)
    def get(self, category, post_uuid):
        """ Gets a specified post by post_uuid """
        response = requests.get('http://post_service:7082/api/' + category + '/' + post_uuid,
                                params=post_get_parser.parse_args())
        return response.json(), response.status_code

    @ns.expect(post_put_model, validate=False)
    def put(self, category, post_uuid):
        """ Updates a post """
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "update"
        request.json["type"] = "post"
        request.json["category"] = category
        request.json["id"] = post_uuid
        deleted_post_event = Event(request.json)
        try:
            db.session.add(deleted_post_event)
            db.session.commit()
            # response = requests.put('http://post_service:7082/api/' + category + '/' + post_uuid, json=request.json)
            # return response.json(), response.status_code
            return "Updated Post Event Created", 200

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500

    def delete(self, category, post_uuid):
        """ Deletes a post """
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "delete"
        request.json["type"] = "post"
        request.json["category"] = category
        request.json["id"] = post_uuid
        deleted_post_event = Event(request.json)
        try:
            db.session.add(deleted_post_event)
            db.session.commit()
            #response = requests.delete('http://post_service:7082/api/' + category + '/' + post_uuid)
            #return response.json(), response.status_code
            return "Deleted Post Event Created", 200

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500


@ns.route('/search/<string:search>')
class PostSearch(Resource):
    @ns.expect(post_get_parser)
    def get(self, category, search):
        """ Searches for posts """
        response = requests.get('http://post_service:7082/api/' + category + '/search/' + search,
                                params=post_get_parser.parse_args())
        return response.json(), response.status_code


@ns.route('/posts/<string:user_uuid>')
class UserPosts(Resource):
    def get(self, category, user_uuid):
        """ Gets all posts by user """
        response = requests.get('http://post_service:7082/api/' + category + '/posts/' + user_uuid)
        return response.json(), response.status_code


@ns.route('/<string:post_uuid>/vote')
class PostVote(Resource):
    @ns.expect(vote_post_model)
    def post(self, category, post_uuid):
        """ Creates a vote on a post """
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "add"
        request.json["type"] = "vote"
        request.json["category"] = category
        request.json["id"] = post_uuid
        updated_vote_event = Event(request.json)
        try:
            db.session.add(updated_vote_event)
            db.session.commit()
            # response = requests.post('http://post_service:7082/api/' + category + '/' + post_uuid + '/vote',
            #                          json=request.json)
            # return response.json(), response.status_code
            return "New Vote Event Created", 200

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500

    @ns.expect(vote_put_model)
    def put(self, category, post_uuid):
        """ Updates a vote on a post """
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "update"
        request.json["type"] = "vote"
        request.json["category"] = category
        request.json["id"] = post_uuid
        updated_vote_event = Event(request.json)
        try:
            db.session.add(updated_vote_event)
            db.session.commit()
            # response = requests.put('http://post_service:7082/api/' + category + '/' + post_uuid + '/vote',
            #                         json=request.json)
            # return response.json(), response.status_code
            return "Updated Vote Event Created", 200

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500

    @ns.expect(vote_delete_model)
    def delete(self, category, post_uuid):
        """ Deletes a vote on a post """
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "delete"
        request.json["type"] = "vote"
        request.json["category"] = category
        request.json["id"] = post_uuid
        deleted_vote_event = Event(request.json)
        try:
            db.session.add(deleted_vote_event)
            db.session.commit()
            # response = requests.delete('http://post_service:7082/api/' + category + '/' + post_uuid + '/vote',
            #                            json=request.json)
            # return response.json(), response.status_code
            return "Deleted Vote Event Created", 200

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500
