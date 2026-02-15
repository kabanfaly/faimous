import uuid
from datetime import datetime
from app import db


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organisation_id = db.Column(db.String(36), db.ForeignKey("organisations.id"), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.String(36), db.ForeignKey("expense_categories.id"), nullable=True, index=True)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    currency = db.Column(db.String(10), nullable=True)
    amount_base = db.Column(db.Numeric(18, 2), nullable=True)
    invoice_file = db.Column(db.String(500), nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
