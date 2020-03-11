from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from . import db


class Comment(db.Model):
    _N = 6

    comment_uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    comment_text = db.Column(db.String())
    top_level_votes = db.Column(db.Integer, default=0)
    comment_votes = db.Column(db.Integer, default=0)
    date_submitted = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    date_edited = db.Column(db.DateTime)
    is_edited = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    author_uuid = db.Column(UUID(as_uuid=True), nullable=False)
    post_uuid = db.Column(UUID(as_uuid=True), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Text, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    nested_level = db.Column(db.Integer)

    def __init__(self, comment_text, author_uuid, post_uuid):
        self.comment_text = comment_text
        self.date_submitted = datetime.utcnow()
        self.author_uuid = author_uuid
        self.post_uuid = post_uuid
        prefix = self.parent.path + '.' if self.parent else ''
        self.path = prefix + '{:0{}d}'.format(self.id, self._N)
        self.nested_level = len(self.path) // self._N - 1

    def __repr__(self):
        return '<Comment {}>'.format(self.comment_text)

    def change_top_level_vote(self, vote):
        for _ in Comment.query.filter(Comment.path.like(self.path + '%')):
            self.top_level_votes = vote
            db.session.add(self)
        db.session.commit()
