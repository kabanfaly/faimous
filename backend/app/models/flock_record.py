import uuid
from datetime import date, datetime
from app import db


class FlockRecord(db.Model):
    __tablename__ = "flock_records"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organisation_id = db.Column(db.String(36), db.ForeignKey("organisations.id"), nullable=False, index=True)
    farm_id = db.Column(db.String(36), db.ForeignKey("farms.id"), nullable=True, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    total_hens = db.Column(db.Integer, nullable=False, default=0)
    dead = db.Column(db.Integer, nullable=False, default=0)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
