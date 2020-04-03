import requests
from flask import request
from flask_restplus import Resource

import datetime
import json
from server.models.event import Event

from server.models.event import db
from server.api.models import *

ns = api.namespace('comments', description='Operations related to server routes')

def createEventJSON(event, operation, type):
    event["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
    event["operation"] = operation
    event["type"] = type
    return event

@ns.route('')
class CommentsCollection(Resource):
    def get(self):
        """ Gets all comments """
        try:
            response = requests.get('http://comment_service:7082/api/comments')
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError as c:
            return {"message": "comment service is unavailable"}, 503


    @ns.expect(comment_model)
    def post(self):
        """ Creates a new comment """
        event_json = createEventJSON(request.json, "add", "comment")
        new_comment_event = Event(event_json)
        try:
            db.session.add(new_comment_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(new_comment_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500


@ns.route('/<string:comment_uuid>')
class PostItem(Resource):
    @ns.expect(comment_put_model, validate=False)
    def put(self, comment_uuid):
        """ Updates a comment """
        event_json = createEventJSON(request.json, "update", "comment")
        event_json["id"] = comment_uuid
        updated_comment_event = Event(event_json)
        try:
            db.session.add(updated_comment_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(updated_comment_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500

    def delete(self, comment_uuid):
        """ Deletes a comment """
        event_json = {}
        event_json = createEventJSON(event_json, "delete", "comment")
        event_json["id"] = comment_uuid
        deleted_comment_event = Event(event_json)
        try:
            db.session.add(deleted_comment_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(deleted_comment_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500


@ns.route('/<string:post_uuid>')
class PostComment(Resource):
    def get(self, post_uuid):
        """ Gets all comments for a post """
        try:
            response = requests.get('http://comment_service:7082/api/comments/post/' + post_uuid)
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError as c:
            return {"message": "comment service is unavailable"}, 503



@ns.route('/user/<string:user_uuid>')
class UserComments(Resource):
    def get(self, user_uuid):
        """ Gets all comments for a user """
        try:
            response = requests.get('http://comment_service:7082/api/comments/user/' + user_uuid)
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError as c:
            return {"message": "comment service is unavailable"}, 503

