from app import db
from app.models import FeedPreparation


def get_organisation_id():
    from app.multi_tenant.context import get_current_organisation_id
    return get_current_organisation_id()


def list_feed_preparations(organisation_id):
    return FeedPreparation.query.filter_by(organisation_id=organisation_id).order_by(FeedPreparation.date.desc()).all()


def create_feed_preparation(organisation_id, data):
    prep = FeedPreparation(
        organisation_id=organisation_id,
        date=data["date"],
        quantity_kg=data["quantity_kg"],
        ratio=data.get("ratio"),
        hens_available=data.get("hens_available"),
        expected_end_date=data.get("expected_end_date"),
        note=data.get("note"),
    )
    db.session.add(prep)
    db.session.commit()
    return prep


def get_feed_preparation(organisation_id, prep_id):
    return FeedPreparation.query.filter_by(id=prep_id, organisation_id=organisation_id).first()


def update_feed_preparation(prep, data):
    if "date" in data:
        prep.date = data["date"]
    if "quantity_kg" in data:
        prep.quantity_kg = data["quantity_kg"]
    if "ratio" in data:
        prep.ratio = data["ratio"]
    if "hens_available" in data:
        prep.hens_available = data["hens_available"]
    db.session.commit()
    return prep


def delete_feed_preparation(prep):
    db.session.delete(prep)
    db.session.commit()
