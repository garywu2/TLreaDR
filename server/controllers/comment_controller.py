import requests
from flask import request
from flask_restplus import Resource

import datetime
import json
from server.models.event import Event

from server.models.event import db
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
        event_json = request.json
        event_json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        event_json["operation"] = "add"
        event_json["type"] = "comment"
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
        event_json = request.json
        event_json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        event_json["operation"] = "update"
        event_json["type"] = "comment"
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
        event_json = json.dumps(event_json)
        event_json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        event_json["operation"] = "delete"
        event_json["type"] = "comment"
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
        response = requests.get('http://comment_service:7082/api/comments/' + post_uuid)
        return response.json(), response.status_code


@ns.route('/user/<string:user_uuid>')
class UserComments(Resource):
    def get(self, user_uuid):
        """ Gets all comments for a user """
        response = requests.get('http://comment_service:7082/api/comments/user/' + user_uuid)
        return response.json(), response.status_code
