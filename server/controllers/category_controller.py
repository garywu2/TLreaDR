import requests
from flask import request
from flask_restplus import Resource

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
        response = requests.post('http://post_service:7082/api/categories', json=request.json)
        return response.json(), response.status_code


@ns.route('/<string:category>')
class CategoryItem(Resource):
    def get(self, category):
        """ Gets a specified category by name """
        response = requests.get('http://post_service:7082/api/categories/' + category)
        return response.json(), response.status_code

    def delete(self, category):
        """ Deletes a category """
        response = requests.delete('http://post_service:7082/api/categories/' + category)
        return response.json(), response.status_code
