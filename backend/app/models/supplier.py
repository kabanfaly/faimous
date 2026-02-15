import uuid
from app import db


class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organisation_id = db.Column(db.String(36), db.ForeignKey("organisations.id"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    city_id = db.Column(db.String(36), db.ForeignKey("cities.id"), nullable=True, index=True)
