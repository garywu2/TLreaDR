import requests
from flask import request
from flask_restplus import Resource

import datetime
import json
from server.models.event import db
from server.models.event import Event
from server.models.api_models import *
from server.parsers.server_parsers import *

ns = api.namespace('users', description='Operations related to users routes')


@ns.route('')
class UserCollection(Resource):
    def get(self):
        """ Gets all users """
        response = requests.get('http://user_service:7082/api/users')
        return response.json(), response.status_code

    @ns.expect(user_model, validate=False)
    def post(self):
        """ Creates a new user """
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "add"
        new_user_event = Event(request.json)
        try:
            db.session.add(new_user_event)
            db.session.commit()
            #response = requests.post('http://user_service:7082/api/users', json=request.json)
            #return response.json(), response.status_code
            return "New User Event Created", 200

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500


@ns.route('/<string:uuid>')
class UserItem(Resource):
    def get(self, uuid):
        """ Gets a specified user by uuid """
        response = requests.get('http://user_service:7082/api/users/' + uuid)
        return response.json(), response.status_code

    @ns.expect(user_put_model, validate=False)
    def put(self, uuid):
        """ Updates a user """
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "update"
        deleted_user_event = Event(request.json)
        try:
            db.session.add(deleted_user_event)
            db.session.commit()
            #response = requests.put('http://user_service:7082/api/users/' + uuid, json=request.json)
            #return response.json(), response.status_code
            return "Updated User Event Created", 200

        except Exception as e:
            return {"message": str(e)}, 500

    def delete(self, uuid):
        """ Deletes a user """
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "delete"
        deleted_user_event = Event(request.json)
        try:
            db.session.add(deleted_user_event)
            db.session.commit()
            #response = requests.delete('http://user_service:7082/api/users/' + uuid)
            #return response.json(), response.status_code
            return "Deleted User Event Created", 200

        except Exception as e:
            return {"message": str(e)}, 500

@ns.route('/login')
class UserLogin(Resource):
    @ns.expect(user_login_parser, validate=False)
    def get(self):
        """ Login for user """
        response = requests.get('http://user_service:7082/api/users/login', params=request.args)
        return response.json(), response.status_code
