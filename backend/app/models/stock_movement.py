import uuid
from datetime import datetime
from app import db


class StockMovement(db.Model):
    __tablename__ = "stock_movements"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = db.Column(db.Date, nullable=False, index=True)
    product_id = db.Column(db.String(36), db.ForeignKey("products.id"), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Numeric(18, 2), nullable=False)
    price = db.Column(db.Numeric(18, 2), nullable=True)
    movement_type = db.Column(db.String(50), nullable=True)
    purchase_id = db.Column(db.String(36), db.ForeignKey("purchases.id"), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
