import requests
from flask import request
from flask_restplus import Resource

import datetime
import json
from server.models.event import db

from server.models.event import Event
from server.models.api_models import *

ns = api.namespace('categories', description='Operations related to category routes')


@ns.route('')
class CategoryCollection(Resource):
    def get(self):
        """ Gets all categories """
        response = requests.get('http://post_service:7082/api/categories')
        return response.json(), response.status_code

    @ns.expect(category_model)
    def post(self):
        """ Creates a new category """
        event_json = request.json
        event_json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        event_json["operation"] = "add"
        event_json["type"] = "category"
        new_category_event = Event(event_json)
        try:
            db.session.add(new_category_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(new_category_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500


@ns.route('/<string:category>')
class CategoryItem(Resource):
    def get(self, category):
        """ Gets a specified category by name """
        response = requests.get('http://post_service:7082/api/categories/' + category)
        return response.json(), response.status_code

    def delete(self, category):
        """ Deletes a category """
        event_json = {}
        event_json = json.dumps(event_json)
        event_json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        event_json["operation"] = "delete"
        event_json["type"] = "category"
        event_json["category"] = category
        deleted_category_event = Event(event_json)
        try:
            db.session.add(deleted_category_event)
            db.session.commit()
            response = requests.get('http://command_service:7082/api/events/' + str(deleted_category_event.event_uuid))
            return response.json(), response.status_code

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500
