import uuid
from datetime import date, datetime
from app import db


class DailyOperation(db.Model):
    __tablename__ = "daily_operations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organisation_id = db.Column(db.String(36), db.ForeignKey("organisations.id"), nullable=False, index=True)
    farm_id = db.Column(db.String(36), db.ForeignKey("farms.id"), nullable=True, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    period = db.Column(db.String(50), nullable=True)
    collect1 = db.Column(db.Integer, nullable=True)
    collect2 = db.Column(db.Integer, nullable=True)
    collect3 = db.Column(db.Integer, nullable=True)
    collect4 = db.Column(db.Integer, nullable=True)
    broken = db.Column(db.Integer, nullable=True)
    hens = db.Column(db.Integer, nullable=True)
    dead = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
