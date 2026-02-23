import uuid
from datetime import date
from decimal import Decimal
from app import db
from app.models.audit_mixin import AuditMixin


class Sale(AuditMixin, db.Model):
    __tablename__ = "sales"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_id = db.Column(db.String(36), db.ForeignKey("farms.id"), nullable=True, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    type = db.Column(db.String(50), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    unit_price = db.Column(db.Numeric(18, 2), nullable=True)
    total_price = db.Column(db.Numeric(18, 2), nullable=True)
    theoretical_price = db.Column(db.Numeric(18, 2), nullable=True)
    price_diff = db.Column(db.Numeric(18, 2), nullable=True)
    wholesaler_id = db.Column(db.String(36), db.ForeignKey("wholesalers.id"), nullable=True, index=True)
    payment_status = db.Column(db.String(50), default="unpaid")
    currency = db.Column(db.String(10), nullable=True)
    amount_base = db.Column(db.Numeric(18, 2), nullable=True)
    payments_received = db.relationship("PaymentReceived", backref="sale", lazy="dynamic", cascade="all, delete-orphan")


class PaymentReceived(AuditMixin, db.Model):
    __tablename__ = "payments_received"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sale_id = db.Column(db.String(36), db.ForeignKey("sales.id"), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=True)
    note = db.Column(db.Text, nullable=True)
