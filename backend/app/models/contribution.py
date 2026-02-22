import uuid
from datetime import datetime
from app import db


class Contribution(db.Model):
    __tablename__ = "contributions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = db.Column(db.Date, nullable=False, index=True)
    shareholder_id = db.Column(db.String(36), db.ForeignKey("shareholders.id"), nullable=True, index=True)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    currency = db.Column(db.String(10), nullable=True)
    amount_base = db.Column(db.Numeric(18, 2), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
