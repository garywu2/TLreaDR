# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime

from . import db


class Post(db.Model):
    post_uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    image_link = db.Column(db.String(1000))

    category_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('category.category_uuid'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    author_uuid = db.Column(UUID(as_uuid=True), nullable=False)

    upvotes = db.Column(db.Integer, nullable=False, default=0)
    downvotes = db.Column(db.Integer, nullable=False, default=0)

    edited_flag = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, title, body, category_uuid, author_uuid, image_link):
        self.title = title
        self.body = body
        self.pub_date = datetime.utcnow()
        self.category_uuid = category_uuid
        self.author_uuid = author_uuid
        self.image_link = image_link

    def __repr__(self):
        return '<Post {}>'.format(self.title)
