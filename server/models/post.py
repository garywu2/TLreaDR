# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime

from . import db


class Post(db.Model):
    post_uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    image_link = db.Column(db.String(2083))

    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    author_uuid = db.Column(UUID(as_uuid=True), nullable=False)

    def __init__(self, title, body, category):
        self.title = title
        self.body = body
        self.pub_date = datetime.utcnow()
        self.category = category

    def __repr__(self):
        return '<Post {}>'.format(self.title)
