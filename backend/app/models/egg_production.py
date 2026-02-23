import uuid
from datetime import date
from app import db
from app.models.audit_mixin import AuditMixin


class EggProduction(AuditMixin, db.Model):
    __tablename__ = "egg_productions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_id = db.Column(db.String(36), db.ForeignKey("farms.id"), nullable=True, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    eggs_count = db.Column(db.Integer, nullable=False, default=0)
    broken_count = db.Column(db.Integer, nullable=False, default=0)
    trays = db.Column(db.Integer, nullable=True)
    remaining = db.Column(db.Integer, nullable=True)
    note = db.Column(db.Text, nullable=True)
