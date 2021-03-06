from datetime import datetime, timedelta
from uuid import uuid4

import requests
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property

from post_service.models import db


class Post(db.Model):
    post_uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    edited_date = db.Column(db.DateTime, default=None)
    image_link = db.Column(db.String(1000))
    article_link = db.Column(db.String(1000))

    category_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('category.category_uuid'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    author_uuid = db.Column(UUID(as_uuid=True), nullable=False)
    author_username = db.Column(db.String(200), nullable=True)

    votes = db.Column(db.Integer, nullable=False, default=0)
    hot_rating = db.Column(db.Float, default=0)

    new_flag = column_property(pub_date > (datetime.utcnow() - timedelta(days=3)))

    edited_flag = db.Column(db.Boolean, nullable=False, default=False)

    hot_flag = db.Column(db.Boolean, default=False)

    def __init__(self, title, body, category_uuid, author_uuid, image_link, article_link):
        self.title = title
        self.body = body
        self.pub_date = datetime.utcnow()
        self.category_uuid = category_uuid
        self.author_uuid = author_uuid
        self.image_link = image_link
        self.article_link = article_link
        # Request made to user_service to obtain author's username
        response = requests.get('http://user_service:7082/api/users/' + str(author_uuid)).json()
        self.author_username = response['username']

    def assign_vote(self, vote_type):
        self.votes += vote_type

    def delete_vote(self, vote_type):
        self.votes -= vote_type

    def __repr__(self):
        return '<Post {}>'.format(self.title)
