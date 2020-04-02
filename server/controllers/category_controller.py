import requests
from flask import request
from flask_restplus import Resource

import datetime
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
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "add"
        request.json["type"] = "category"
        new_user_event = Event(request.json)
        try:
            db.session.add(new_user_event)
            db.session.commit()
            #response = requests.post('http://post_service:7082/api/categories', json=request.json)
            #return response.json(), response.status_code
            return "New Category Event Created", 200

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
        request.json["time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        request.json["operation"] = "delete"
        request.json["type"] = "category"
        request.json["category"] = category
        new_user_event = Event(request.json)
        try:
            db.session.add(new_user_event)
            db.session.commit()
            #response = requests.delete('http://post_service:7082/api/categories/' + category)
            #return response.json(), response.status_code
            return "Deleted Category Event Created", 200

        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 500
