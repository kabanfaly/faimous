from app import db
from app.models import Wholesaler, City


def list_wholesalers(organisation_id):
    return (
        Wholesaler.query.join(City, Wholesaler.city_id == City.id)
        .filter(City.organisation_id == organisation_id)
        .order_by(Wholesaler.name)
        .all()
    )


def create_wholesaler(organisation_id, data):
    wholesaler = Wholesaler(
        name=data["name"],
        city_id=data.get("city_id"),
    )
    db.session.add(wholesaler)
    db.session.commit()
    return wholesaler


def get_wholesaler(organisation_id, wholesaler_id):
    return (
        Wholesaler.query.join(City, Wholesaler.city_id == City.id)
        .filter(Wholesaler.id == wholesaler_id, City.organisation_id == organisation_id)
        .first()
    )


def update_wholesaler(wholesaler, data):
    if "name" in data:
        wholesaler.name = data["name"]
    if "city_id" in data:
        wholesaler.city_id = data["city_id"]
    db.session.commit()
    return wholesaler


def delete_wholesaler(wholesaler):
    db.session.delete(wholesaler)
    db.session.commit()
