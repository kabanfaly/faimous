import uuid
from app import db


class City(db.Model):
    __tablename__ = "cities"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organisation_id = db.Column(db.String(36), db.ForeignKey("organisations.id"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    prefecture = db.Column(db.String(255), nullable=True)
