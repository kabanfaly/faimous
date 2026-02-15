from app import db
from app.models import Farm


def list_farms(organisation_id):
    return Farm.query.filter_by(organisation_id=organisation_id).order_by(Farm.name).all()


def create_farm(organisation_id, data):
    farm = Farm(
        organisation_id=organisation_id,
        name=data["name"],
        location=data.get("location"),
    )
    db.session.add(farm)
    db.session.commit()
    return farm


def get_farm(organisation_id, farm_id):
    return Farm.query.filter_by(id=farm_id, organisation_id=organisation_id).first()


def update_farm(farm, data):
    if "name" in data:
        farm.name = data["name"]
    if "location" in data:
        farm.location = data["location"]
    db.session.commit()
    return farm


def delete_farm(farm):
    db.session.delete(farm)
    db.session.commit()
