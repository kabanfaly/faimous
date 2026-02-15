from app import db
from app.models import Shareholder


def list_shareholders(organisation_id):
    return Shareholder.query.filter_by(organisation_id=organisation_id).order_by(Shareholder.last_name).all()


def create_shareholder(organisation_id, data):
    shareholder = Shareholder(
        organisation_id=organisation_id,
        first_name=data["first_name"],
        last_name=data["last_name"],
        phone=data.get("phone"),
        email=data.get("email"),
    )
    db.session.add(shareholder)
    db.session.commit()
    return shareholder


def get_shareholder(organisation_id, shareholder_id):
    return Shareholder.query.filter_by(id=shareholder_id, organisation_id=organisation_id).first()


def update_shareholder(shareholder, data):
    if "first_name" in data:
        shareholder.first_name = data["first_name"]
    if "last_name" in data:
        shareholder.last_name = data["last_name"]
    if "phone" in data:
        shareholder.phone = data["phone"]
    if "email" in data:
        shareholder.email = data["email"]
    db.session.commit()
    return shareholder


def delete_shareholder(shareholder):
    db.session.delete(shareholder)
    db.session.commit()
