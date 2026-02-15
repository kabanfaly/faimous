from app import db
from app.models import City


def list_cities(organisation_id):
    return City.query.filter_by(organisation_id=organisation_id).order_by(City.name).all()


def create_city(organisation_id, data):
    city = City(
        organisation_id=organisation_id,
        name=data["name"],
        prefecture=data.get("prefecture"),
    )
    db.session.add(city)
    db.session.commit()
    return city


def get_city(organisation_id, city_id):
    return City.query.filter_by(id=city_id, organisation_id=organisation_id).first()


def update_city(city, data):
    if "name" in data:
        city.name = data["name"]
    if "prefecture" in data:
        city.prefecture = data["prefecture"]
    db.session.commit()
    return city


def delete_city(city):
    db.session.delete(city)
    db.session.commit()
