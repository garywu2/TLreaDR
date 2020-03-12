import json
import requests
from flask_restplus import Resource, fields, reqparse, marshal

from server.api.restplus import api

ns = api.namespace('news', description='Operations related to news service')

category_parser = reqparse.RequestParser()
category_parser.add_argument('name', required=True, type=str, help='name of category', location='json')

url = ('http://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=b511c877204a447b8ae3d01af4b875b3')

@ns.route('')
class CategoryCollection(Resource):
    def get(self):
        """
        Gets all top news articles
        """
        results = requests.get(url)
        return results.json(), 200
