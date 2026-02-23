import uuid
from app import db
from app.models.audit_mixin import AuditMixin


class Wholesaler(AuditMixin, db.Model):
    __tablename__ = "wholesalers"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    city_id = db.Column(db.String(36), db.ForeignKey("cities.id"), nullable=True, index=True)
