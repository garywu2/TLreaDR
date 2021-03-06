import requests
from flask import request
from flask_restplus import Resource

import datetime
import json
from server.models.event import db
from server.models.event import Event
from server.api.models import *
from server.parsers.server_parsers import *

ns = api.namespace('users', description='Operations related to users routes')

def createEventJSON(event, operation, type):
    event["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
    event["operation"] = operation
    event["type"] = type
    return event

@ns.route('')
class UserCollection(Resource):
    def get(self):
        """ Gets all users """
        try:
            response = requests.get('http://user_service:7082/api/users')
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError as c:
            return {"message": "user service is unavailable"}, 503
    @ns.expect(user_model, validate=False)
    def post(self):
        """ Creates a new user """
        event_json = createEventJSON(request.json, "add", "user")
        new_user_event = Event(event_json)
        try:
            db.session.add(new_user_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(new_user_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500


@ns.route('/<string:uuid>')
class UserItem(Resource):
    def get(self, uuid):
        """ Gets a specified user by uuid """
        try:
            response = requests.get('http://user_service:7082/api/users/' + uuid)
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError as c:
            return {"message": "user service is unavailable"}, 503
    @ns.expect(user_put_model, validate=False)
    def put(self, uuid):
        """ Updates a user """
        event_json = createEventJSON(request.json, "update", "user")
        event_json["id"] = uuid
        updated_user_event = Event(event_json)
        try:
            db.session.add(updated_user_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(updated_user_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            return {"message": str(e)}, 500

    def delete(self, uuid):
        """ Deletes a user """
        event_json = createEventJSON(request.json, "delete", "user")
        event_json["id"] = uuid
        deleted_user_event = Event(event_json)
        try:
            db.session.add(deleted_user_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(deleted_user_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            return {"message": str(e)}, 500

@ns.route('/login')
class UserLogin(Resource):
    @ns.expect(user_login_parser, validate=False)
    def get(self):
        """ Login for user """
        try:
            response = requests.get('http://user_service:7082/api/users/login', params=request.args)
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError as c:
            return {"message": "user service is unavailable"}, 503