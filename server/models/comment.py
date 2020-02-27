from datetime import datetime

from . import db


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String())
    date_submitted = db.Column(db.DateTime)
    date_edited = db.Column(db.DateTime)
    is_edited = db.Column(db.Boolean)
    is_deleted = db.Column(db.Boolean)

    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    post = db.relationship('Post', backref=db.backref('post', lazy='dynamic'))

    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.comment_id'))
    parent_comment = db.relationship('Comment', backref=db.backref('comment', lazy='dynamic'))

    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    author = db.relationship('User', backref=db.backref('user', lazy='dynamic'))

    def __init__(self, comment_text, post, parent_comment, author):
        self.comment_text = comment_text
        self.date_submitted = datetime.utcnow()
        self.post = post
        self.parent_comment = parent_comment
        self.author = author

    def __repr__(self):
        return '<Comment {}>'.format(self.comment_text)
