from flask_restplus import fields

from post_service.api.restplus import api

post_dto = api.model('post', {
    'post_uuid': fields.String(required=True, description='post uuid'),
    'title': fields.String(required=True, description='title of the post'),
    'body': fields.String(required=True, description='body of the post'),
    'pub_date': fields.String(required=True, description='published date'),
    'edited_date': fields.String(description='published date'),
    'image_link': fields.String(description='image link of the post'),
    'article_link': fields.String(description='article link of the post'),
    'votes': fields.Integer(required=True, description='votes of the post'),
    'hot_rating': fields.Float(required=True, description='rating for hotness of the post'),
    'category_uuid': fields.String(required=True, description='category uuid'),
    'category': fields.String(required=True, description='category of the post'),
    'author_uuid': fields.String(required=True, description='uuid of author'),
    'author_username': fields.String(required=True, description='username of author'),
    'new_flag': fields.Boolean(required=True, description='new flag for the post'),
    'edited_flag': fields.Boolean(required=True, description='new flag for the post'),
    'vote_type': fields.Integer(required=False, description='status of user vote')
})

category_dto = api.model('category', {
    'category_uuid': fields.String(required=True, description='category uuid'),
    'name': fields.String(required=True, description='category name'),
})