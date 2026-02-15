import uuid
from datetime import date, datetime
from app import db


class FeedPreparation(db.Model):
    __tablename__ = "feed_preparations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organisation_id = db.Column(db.String(36), db.ForeignKey("organisations.id"), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    quantity_kg = db.Column(db.Numeric(18, 2), nullable=False)
    ratio = db.Column(db.String(100), nullable=True)
    hens_available = db.Column(db.Integer, nullable=True)
    expected_end_date = db.Column(db.Date, nullable=True)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
