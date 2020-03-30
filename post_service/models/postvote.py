from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from post_service.models import db


class Postvote(db.Model):
    post_uuid = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    user_uuid = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    vote_type = db.Column(db.Integer, nullable=True)

    def __init__(self, post_uuid, user_uuid, vote_type):
        self.post_uuid = post_uuid
        self.user_uuid = user_uuid
        self.vote_type = vote_type

    def __repr__(self):
        return self.post_uuid + " " + self.user_uuid + " " + self.vote_type