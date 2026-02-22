from app import db
from app.models import Farm


def list_farms():
    return Farm.query.order_by(Farm.name).all()


def create_farm(data):
    farm = Farm(
        name=data["name"],
        city_id=data.get("city_id"),
    )
    db.session.add(farm)
    db.session.commit()
    return farm


def get_farm(farm_id):
    return Farm.query.filter_by(id=farm_id).first()


def update_farm(farm, data):
    if "name" in data:
        farm.name = data["name"]
    if "city_id" in data:
        farm.city_id = data["city_id"]
    db.session.commit()
    return farm


def delete_farm(farm):
    db.session.delete(farm)
    db.session.commit()
