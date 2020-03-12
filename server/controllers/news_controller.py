import json
import requests
from flask_restplus import Resource, fields, reqparse, marshal

from server.api.restplus import api

ns = api.namespace('news', description='Operations related to news service')

news_search_parser = reqparse.RequestParser()
news_search_parser.add_argument('keyword', required=True, type=str, help='search term', location='json')

@ns.route('')
class CategoryCollection(Resource):
    def get(self):
        """
        Gets all top news articles
        """
        url = ('http://newsapi.org/v2/top-headlines?'
               'country=us&'
               'apiKey=b511c877204a447b8ae3d01af4b875b3')
        results = requests.get(url)
        return results.json(), 200

    @api.expect(news_search_parser)
    def post(self):
        """
        Search by key word
        """
        args = news_search_parser.parse_args()
        url = ('http://newsapi.org/v2/everything?'
               'q=' + args['keyword'] + '&'
               'from=2020-03-12&'
               'sortBy=popularity&'
               'apiKey=b511c877204a447b8ae3d01af4b875b3')
        results = requests.get(url)
        return results.json(), 200
