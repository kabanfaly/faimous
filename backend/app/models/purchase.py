import uuid
from datetime import datetime
from app import db


class Purchase(db.Model):
    __tablename__ = "purchases"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = db.Column(db.Date, nullable=False, index=True)
    supplier_id = db.Column(db.String(36), db.ForeignKey("suppliers.id"), nullable=True, index=True)
    product_id = db.Column(db.String(36), db.ForeignKey("products.id"), nullable=True, index=True)
    unit_price = db.Column(db.Numeric(18, 2), nullable=True)
    quantity = db.Column(db.Numeric(18, 2), nullable=False, default=0)
    total_price = db.Column(db.Numeric(18, 2), nullable=True)
    status = db.Column(db.String(50), default="unpaid")
    currency = db.Column(db.String(10), nullable=True)
    amount_base = db.Column(db.Numeric(18, 2), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    supplier_payments = db.relationship("SupplierPayment", backref="purchase", lazy="dynamic", cascade="all, delete-orphan")


class SupplierPayment(db.Model):
    __tablename__ = "supplier_payments"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    purchase_id = db.Column(db.String(36), db.ForeignKey("purchases.id"), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=True)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
