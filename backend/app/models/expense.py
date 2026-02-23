import uuid
from app import db
from app.models.audit_mixin import AuditMixin


class Expense(AuditMixin, db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_id = db.Column(db.String(36), db.ForeignKey("farms.id"), nullable=True, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.String(36), db.ForeignKey("expense_categories.id"), nullable=True, index=True)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    currency = db.Column(db.String(10), nullable=True)
    amount_base = db.Column(db.Numeric(18, 2), nullable=True)
    invoice_file = db.Column(db.String(500), nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
