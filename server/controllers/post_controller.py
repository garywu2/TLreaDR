import requests
from flask import request
from flask_restplus import Resource

import datetime
import json
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
        response = requests.get('http//post_service:7082/api/' + category + '/posts',
                                params=post_get_parser.parse_args())
        return response.json(), response.status_code

    @ns.expect(post_model, validate=False)
    def post(self, category):
        """ Creates a new post """
        event_json = request.json
        event_json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        event_json["operation"] = "add"
        event_json["type"] = "post"
        event_json["category"] = category
        new_post_event = Event(event_json)
        try:
            db.session.add(new_post_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/' + str(new_post_event.event_uuid))
            return response.json(), response.status_code

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
        event_json = request.json
        event_json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        event_json["operation"] = "update"
        event_json["type"] = "post"
        event_json["category"] = category
        event_json["id"] = post_uuid
        updated_post_event = Event(event_json)
        try:
            db.session.add(updated_post_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/' + str(updated_post_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500

    def delete(self, category, post_uuid):
        """ Deletes a post """
        event_json = request.json
        event_json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        event_json["operation"] = "delete"
        event_json["type"] = "post"
        event_json["category"] = category
        event_json["id"] = post_uuid
        deleted_post_event = Event(event_json)
        try:
            db.session.add(deleted_post_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/' + str(deleted_post_event.event_uuid))
            return response.json(), response.status_code

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
        event_json = request.json
        event_json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        event_json["operation"] = "add"
        event_json["type"] = "vote"
        event_json["category"] = category
        event_json["id"] = post_uuid
        new_vote_event = Event(event_json)
        try:
            db.session.add(new_vote_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/' + str(new_vote_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500

    @ns.expect(vote_put_model)
    def put(self, category, post_uuid):
        """ Updates a vote on a post """
        event_json = request.json
        event_json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        event_json["operation"] = "update"
        event_json["type"] = "vote"
        event_json["category"] = category
        event_json["id"] = post_uuid
        updated_vote_event = Event(event_json)
        try:
            db.session.add(updated_vote_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/' + str(updated_vote_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500

    @ns.expect(vote_delete_model)
    def delete(self, category, post_uuid):
        """ Deletes a vote on a post """
        event_json = request.json
        event_json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        event_json["operation"] = "delete"
        event_json["type"] = "vote"
        event_json["category"] = category
        event_json["id"] = post_uuid
        deleted_vote_event = Event(event_json)
        try:
            db.session.add(deleted_vote_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/' + str(deleted_vote_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500
