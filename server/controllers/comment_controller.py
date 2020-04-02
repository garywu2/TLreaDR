import requests
from flask import request
from flask_restplus import Resource

import datetime
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
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "add"
        request.json["type"] = "comment"
        new_comment_event = Event(request.json)
        try:
            db.session.add(new_comment_event)
            db.session.commit()
            #response = requests.post('http://comment_service:7082/api/comments', json=request.json)
            #return response.json(), response.status_code
            return "New Comment Event Created", 200

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500


@ns.route('/<string:comment_uuid>')
class PostItem(Resource):
    @ns.expect(comment_put_model, validate=False)
    def put(self, comment_uuid):
        """ Updates a comment """
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "update"
        request.json["type"] = "comment"
        request.json["id"] = comment_uuid
        updated_comment_event = Event(request.json)
        try:
            db.session.add(updated_comment_event)
            db.session.commit()
            #response = requests.put('http://comment_service:7082/api/comments/' + comment_uuid, json=request.json)
            #return response.json(), response.status_code
            return "Updated Comment Event Created", 200

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500

    def delete(self, comment_uuid):
        """ Deletes a comment """
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "delete"
        request.json["type"] = "comment"
        request.json["id"] = comment_uuid
        deleted_comment_event = Event(request.json)
        try:
            db.session.add(deleted_comment_event)
            db.session.commit()
            #response = requests.delete('http://comment_service:7082/api/comments/' + comment_uuid)
            #return response.json(), response.status_code
            return "Deleted Comment Event Created", 200

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
