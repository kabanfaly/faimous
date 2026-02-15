from app import db
from app.models import User


def get_organisation_id():
    from app.multi_tenant.context import get_current_organisation_id
    return get_current_organisation_id()


def list_users(organisation_id):
    return User.query.filter_by(organisation_id=organisation_id).order_by(User.email).all()


def create_user(organisation_id, data):
    if User.query.filter_by(email=data["email"]).first():
        return None, "Email already exists"
    user = User(
        organisation_id=organisation_id,
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        gender=data.get("gender", "male"),
        language=data.get("language", "fr"),
        role=data.get("role", "user"),
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return user, None


def get_user(organisation_id, user_id):
    return User.query.filter_by(id=user_id, organisation_id=organisation_id).first()


def update_user(user, data):
    if "first_name" in data:
        user.first_name = data["first_name"]
    if "last_name" in data:
        user.last_name = data["last_name"]
    if "gender" in data:
        user.gender = data["gender"]
    if "language" in data:
        user.language = data["language"]
    if "activated" in data:
        user.activated = data["activated"]
    if "role" in data:
        user.role = data["role"]
    db.session.commit()
    return user
