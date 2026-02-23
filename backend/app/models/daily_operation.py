import uuid
from datetime import date
from app import db
from app.models.audit_mixin import AuditMixin


class DailyOperation(AuditMixin, db.Model):
    __tablename__ = "daily_operations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
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
