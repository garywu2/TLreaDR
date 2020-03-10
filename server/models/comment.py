from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from . import db


class Comment(db.Model):
    comment_uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    comment_text = db.Column(db.String())
    date_submitted = db.Column(db.DateTime)
    date_edited = db.Column(db.DateTime)
    is_edited = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    author_uuid = db.Column(UUID(as_uuid=True), nullable=False)
    parent_uuid = db.Column(UUID(as_uuid=True), nullable=False)

    post_flag = db.Column(db.Boolean, nullable=False)

    def __init__(self, comment_text, author_uuid, parent_uuid):
        self.comment_text = comment_text
        self.date_submitted = datetime.utcnow()
        self.author_uuid = author_uuid
        self.parent_uuid = parent_uuid


    def __repr__(self):
        return '<Comment {}>'.format(self.comment_text)
