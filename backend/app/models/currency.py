from app import db
from app.models.audit_mixin import AuditMixin


class Currency(AuditMixin, db.Model):
    __tablename__ = "currencies"

    code = db.Column(db.String(10), primary_key=True)
    symbol = db.Column(db.String(10), nullable=True)


class ExchangeRate(AuditMixin, db.Model):
    __tablename__ = "exchange_rates"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_currency = db.Column(db.String(10), db.ForeignKey("currencies.code"), nullable=False, index=True)
    to_currency = db.Column(db.String(10), db.ForeignKey("currencies.code"), nullable=False, index=True)
    rate = db.Column(db.Numeric(18, 6), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
