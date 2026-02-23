import uuid
from app import db
from app.models.audit_mixin import AuditMixin


class ExpenseCategory(AuditMixin, db.Model):
    __tablename__ = "expense_categories"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organisation_id = db.Column(db.String(36), db.ForeignKey("organisations.id"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
