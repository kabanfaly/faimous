import uuid
from app import db


class Farm(db.Model):
    __tablename__ = "farms"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organisation_id = db.Column(db.String(36), db.ForeignKey("organisations.id"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
