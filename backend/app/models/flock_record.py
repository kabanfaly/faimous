import uuid
from datetime import date
from app import db
from app.models.audit_mixin import AuditMixin


class FlockRecord(AuditMixin, db.Model):
    __tablename__ = "flock_records"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_id = db.Column(db.String(36), db.ForeignKey("farms.id"), nullable=True, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    total_hens = db.Column(db.Integer, nullable=False, default=0)
    dead = db.Column(db.Integer, nullable=False, default=0)
    note = db.Column(db.Text, nullable=True)
