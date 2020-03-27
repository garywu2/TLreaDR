from post_service.models import db

from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class Category(db.Model):
    category_uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category {}>'.format(self.name)
