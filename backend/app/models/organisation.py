import uuid
from datetime import datetime
from app import db


class Organisation(db.Model):
    __tablename__ = "organisations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    currency_default = db.Column(db.String(10), default="GNF")
    language_default = db.Column(db.String(10), default="fr")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship("User", backref="organisation", lazy="dynamic")
    farms = db.relationship("Farm", backref="organisation", lazy="dynamic")
