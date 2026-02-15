from app import db
from app.models import Contribution, Shareholder


def get_organisation_id():
    from app.multi_tenant.context import get_current_organisation_id
    return get_current_organisation_id()


def list_contributions(organisation_id):
    return Contribution.query.filter_by(organisation_id=organisation_id).order_by(Contribution.date.desc()).all()


def create_contribution(organisation_id, data):
    contrib = Contribution(
        organisation_id=organisation_id,
        date=data["date"],
        shareholder_id=data.get("shareholder_id"),
        amount=data["amount"],
        currency=data.get("currency"),
        amount_base=data.get("amount_base"),
        description=data.get("description"),
    )
    db.session.add(contrib)
    db.session.commit()
    return contrib


def get_contribution(organisation_id, contribution_id):
    return Contribution.query.filter_by(id=contribution_id, organisation_id=organisation_id).first()


def update_contribution(contrib, data):
    if "date" in data:
        contrib.date = data["date"]
    if "shareholder_id" in data:
        contrib.shareholder_id = data["shareholder_id"]
    if "amount" in data:
        contrib.amount = data["amount"]
    if "description" in data:
        contrib.description = data["description"]
    db.session.commit()
    return contrib


def delete_contribution(contrib):
    db.session.delete(contrib)
    db.session.commit()


def list_shareholders(organisation_id):
    return Shareholder.query.filter_by(organisation_id=organisation_id).order_by(Shareholder.last_name).all()


def create_shareholder(organisation_id, data):
    sh = Shareholder(
        organisation_id=organisation_id,
        first_name=data["first_name"],
        last_name=data["last_name"],
        phone=data.get("phone"),
        email=data.get("email"),
    )
    db.session.add(sh)
    db.session.commit()
    return sh
