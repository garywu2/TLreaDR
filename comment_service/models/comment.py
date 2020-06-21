from datetime import datetime
from uuid import uuid4

import requests
from sqlalchemy.dialects.postgresql import UUID

from . import db

class Comment(db.Model):
    _N = 6

    comment_uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    comment_text = db.Column(db.String())
    comment_upvotes = db.Column(db.Integer, default=0)
    comment_downvotes = db.Column(db.Integer, default=0)
    votes = db.Column(db.Integer, default=0)
    date_submitted = db.Column(db.DateTime(), default=datetime.utcnow)
    date_edited = db.Column(db.DateTime)
    is_edited = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    author_uuid = db.Column(UUID(as_uuid=True), nullable=False)
    author_username = db.Column(db.String(), nullable=True)
    post_uuid = db.Column(UUID(as_uuid=True), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    path = db.Column(db.Text, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    comment_level = db.Column(db.Integer, default=0)

    def __init__(self, comment_text, author_uuid, post_uuid, parent_id):
        self.comment_text = comment_text
        self.date_submitted = datetime.utcnow()
        self.author_uuid = author_uuid
        self.post_uuid = post_uuid
        self.parent_id = parent_id
        # Request made to user_service to obtain author's username
        response = requests.get('http://user_service:7082/api/users/' + str(author_uuid)).json()
        self.author_username = response['username']

    def __repr__(self):
        return '<Comment {}>'.format(self.comment_text)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def make_path(self):
        parent = Comment.query.filter_by(id=self.parent_id).first()
        if parent:
            prefix = parent.path + '.'
        else:
            prefix = ''
        self.path = prefix + '{:0{}d}'.format(self.id, self._N)
        self.comment_level = self.level()

    def level(self):
        return len(self.path) // self._N - 1

    def assign_vote(self, vote_type):
        self.votes += vote_type

    def delete_vote(self, vote_type):
        self.votes -= vote_type
