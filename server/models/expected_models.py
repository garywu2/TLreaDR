from flask_restplus import fields

from server.api.restplus import api

# Models

user_model = api.model('User', {
    "email": fields.String(description='email'),
    "username": fields.String(description='username'),
    "password": fields.String(description='password'),
})

user_put_model = api.model('User', {
    "new_email": fields.String(description='new email of user'),
    "new_username": fields.String(description='new username of user'),
    "new_password": fields.String(description='new password of user'),
})

post_model = api.model('Post', {
    "title": fields.String(description='title of post'),
    "body": fields.String(description='body of post'),
    "image_link": fields.String(description='image link to picture'),
    "author_uuid": fields.String(description='uuid of author'),
})

post_put_model = api.model('Post', {
    "new_title": fields.String(description='new title of post'),
    "new_body": fields.String(description='new body of post'),
    "new_image_link": fields.String(description='new image link to picture'),
})

category_model = api.model('Category', {
    "name": fields.String(description='category name')
})

comment_model = api.model('Comment', {
    "text": fields.String(description='text of comment'),
    "author_uuid": fields.String(description='author uuid of comment'),
    "post_uuid": fields.String(description='post uuid of comment'),
    "parent_id": fields.String(description='parent id of comment'),
})

comment_put_model = api.model('Comment', {
    "new_text": fields.String(description='new text of comment'),
})