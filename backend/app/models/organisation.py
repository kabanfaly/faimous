import uuid
from app import db
from app.models.audit_mixin import AuditMixin


class Organisation(AuditMixin, db.Model):
    __tablename__ = "organisations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    currency_default = db.Column(db.String(10), default="GNF")
    language_default = db.Column(db.String(10), default="fr")
    users = db.relationship("User", backref="organisation", lazy="dynamic")
