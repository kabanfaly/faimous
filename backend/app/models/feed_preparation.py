import uuid
from datetime import date
from app import db
from app.models.audit_mixin import AuditMixin


class FeedPreparation(AuditMixin, db.Model):
    __tablename__ = "feed_preparations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organisation_id = db.Column(db.String(36), db.ForeignKey("organisations.id"), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    quantity_kg = db.Column(db.Numeric(18, 2), nullable=False)
    ratio = db.Column(db.String(100), nullable=True)
    hens_available = db.Column(db.Integer, nullable=True)
    expected_end_date = db.Column(db.Date, nullable=True)
    note = db.Column(db.Text, nullable=True)
