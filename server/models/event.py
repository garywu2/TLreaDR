from . import db

from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class Event(db.Model):
    event_uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    event_blob = db.Column(db.JSON)

    def __init__(self, event_blob):
        self.event_blob = event_blob

    def __repr__(self):
        return '<Event {}>'.format(self.blob)
