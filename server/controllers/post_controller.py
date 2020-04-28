import requests
from flask import request
from flask_restplus import Resource

import datetime
import json
from server.models.event import db
from server.models.event import Event

from server.api.models import *
from server.parsers.server_parsers import *

ns = api.namespace('posts', description='Operations related to post routes', path="/<string:category>")

def createEventJSON(event, operation, type, category):
    event["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
    event["operation"] = operation
    event["type"] = type
    event["category"] = category
    return event

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
        event_json = createEventJSON(request.json, "add", "post", category)
        new_post_event = Event(event_json)
        try:
            db.session.add(new_post_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(new_post_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500


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
        event_json = createEventJSON(request.json, "update", "post", category)
        event_json["id"] = post_uuid
        updated_post_event = Event(event_json)
        try:
            db.session.add(updated_post_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(updated_post_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500

    def delete(self, category, post_uuid):
        """ Deletes a post """
        event_json = {}
        event_json = createEventJSON(event_json, "delete", "post", category)
        event_json["id"] = post_uuid
        deleted_post_event = Event(event_json)
        try:
            db.session.add(deleted_post_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(deleted_post_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500


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
        event_json = createEventJSON(request.json, "add", "vote", category)
        event_json["id"] = post_uuid
        new_vote_event = Event(event_json)
        try:
            db.session.add(new_vote_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(new_vote_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500

    @ns.expect(vote_put_model)
    def put(self, category, post_uuid):
        """ Updates a vote on a post """
        event_json = createEventJSON(request.json, "update", "vote", category)
        event_json["id"] = post_uuid
        updated_vote_event = Event(event_json)
        try:
            db.session.add(updated_vote_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(updated_vote_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500

    @ns.expect(vote_delete_model)
    def delete(self, category, post_uuid):
        """ Deletes a vote on a post """
        event_json = createEventJSON(request.json, "delete", "vote", category)
        event_json["id"] = post_uuid
        deleted_vote_event = Event(event_json)
        try:
            db.session.add(deleted_vote_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(deleted_vote_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500

@ns.route('/summarize')
class PostSummarize(Resource):
    @ns.expect(article_summarize_parser)
    def get(self, category):
        """
        Summarizes an article
        """
        try:
            args = article_summarize_parser.parse_args()
            response = requests.get('http://post_service:7082/api/all/summarize', params=args)
            return response.json(), response.status_code
        except Exception as e:
            return {"message": str(e)}, 500