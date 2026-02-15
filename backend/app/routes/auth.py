import logging
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from marshmallow import ValidationError

from app import db, jwt, limiter
from app.models import User, Organisation
from app.schemas.auth import (
    LoginSchema,
    RegisterSchema,
    UserSchema,
    OrganisationSchema,
    UpdateProfileSchema,
    ChangePasswordSchema,
)
from app.multi_tenant.context import set_current_organisation_id

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)
login_schema = LoginSchema()
register_schema = RegisterSchema()
user_schema = UserSchema()
organisation_schema = OrganisationSchema()
update_profile_schema = UpdateProfileSchema()
change_password_schema = ChangePasswordSchema()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.get("id") if isinstance(user, dict) else str(user.id)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = User.query.get(identity)
    if user:
        set_current_organisation_id(user.organisation_id)
    return user


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = login_schema.load(request.get_json() or {})
    except ValidationError as e:
        logger.error    ("Login validation failed: %s", e.messages)
        return jsonify({"errors": e.messages}), 400
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        logger.info("Login failed for email=%s (invalid credentials)", data["email"])
        return jsonify({"message": "Invalid email or password"}), 401
    if not user.activated:
        logger.error("Login denied for email=%s (account not activated)", data["email"])
        return jsonify({"message": "Account is not active"}), 403
    org = Organisation.query.get(user.organisation_id)
    access_token = create_access_token(
        identity=user,
        additional_claims={
            "organisation_id": user.organisation_id,
            "role": user.role,
        },
    )
    logger.info("Login success user_id=%s email=%s", user.id, user.email)
    return jsonify(
        {
            "access_token": access_token,
            "user": user_schema.dump(user),
            "organisation": organisation_schema.dump(org),
        }
    )


@auth_bp.route("/register", methods=["POST"])
@limiter.limit(
    "5 per minute",
    error_message="Too many registration attempts. Please wait before trying again.",
)
def register():
    try:
        data = register_schema.load(request.get_json() or {})
    except ValidationError as e:
        logger.warning("Register validation failed: %s", e.messages)
        return jsonify({"errors": e.messages}), 400
    if User.query.filter_by(email=data["email"]).first():
        logger.info("Register failed: email already exists email=%s", data["email"])
        return jsonify({"message": "Email already registered"}), 409
    org = Organisation(
        name=data["organisation_name"],
        currency_default="GNF",
        language_default="fr",
    )
    db.session.add(org)
    db.session.flush()
    user = User(
        organisation_id=org.id,
        email=data["email"],
        first_name=data.get("first_name") or data["email"].split("@")[0],
        last_name=data.get("last_name") or "",
        role="owner",
        activated=True,
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(
        identity=user,
        additional_claims={
            "organisation_id": org.id,
            "role": user.role,
        },
    )
    logger.info("Register success user_id=%s email=%s org=%s", user.id, user.email, org.name)
    return jsonify(
        {
            "access_token": access_token,
            "user": user_schema.dump(user),
            "organisation": organisation_schema.dump(org),
        }
    ), 201


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        logger.warning("Auth /me: user not found user_id=%s", user_id)
        return jsonify({"message": "User not found"}), 404
    org = Organisation.query.get(user.organisation_id)
    return jsonify(
        {
            "user": user_schema.dump(user),
            "organisation": organisation_schema.dump(org),
        }
    )


@auth_bp.route("/me", methods=["PATCH"])
@jwt_required()
def update_me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    try:
        data = update_profile_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    if not data:
        return jsonify({"user": user_schema.dump(user), "organisation": organisation_schema.dump(Organisation.query.get(user.organisation_id))})
    if "email" in data and data["email"] != user.email:
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"message": "Email already registered", "errors": {"email": ["Already in use"]}}), 409
        user.email = data["email"]
    if "first_name" in data:
        user.first_name = data["first_name"]
    if "last_name" in data:
        user.last_name = data["last_name"]
    db.session.commit()
    org = Organisation.query.get(user.organisation_id)
    logger.info("Profile updated user_id=%s", user_id)
    return jsonify(
        {
            "user": user_schema.dump(user),
            "organisation": organisation_schema.dump(org),
        }
    )


@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    try:
        data = change_password_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    if not user.check_password(data["current_password"]):
        return jsonify({"message": "Current password is incorrect", "errors": {"current_password": ["Incorrect"]}}), 400
    user.set_password(data["new_password"])
    db.session.commit()
    logger.info("Password changed user_id=%s", user_id)
    return jsonify({"message": "Password updated"})
