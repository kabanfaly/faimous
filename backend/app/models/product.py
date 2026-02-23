import uuid
from app import db
from app.models.audit_mixin import AuditMixin


class Product(AuditMixin, db.Model):
    __tablename__ = "products"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_type_id = db.Column(db.String(36), db.ForeignKey("product_types.id"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Numeric(18, 2), nullable=True)
    unit = db.Column(db.String(50), nullable=True)

    product_type = db.relationship("ProductType", backref="products", lazy="joined")
