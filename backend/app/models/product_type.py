import uuid
from app import db


class ProductType(db.Model):
    __tablename__ = "product_types"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False, unique=True)
    farm_id = db.Column(db.String(36), db.ForeignKey("farms.id"), nullable=False, index=True)

    farm = db.relationship("Farm", backref="product_types")
