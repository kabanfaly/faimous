import logging
import os
from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded

from config import config_by_name

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)


def make_celery_extension(flask_app):
    from app.celery_app import make_celery
    celery = make_celery(flask_app)
    flask_app.extensions["celery"] = celery
    return celery


def configure_logging(flask_app):
    level = logging.DEBUG if flask_app.debug else logging.INFO
    flask_app.logger.setLevel(level)
    for handler in flask_app.logger.handlers[:]:
        flask_app.logger.removeHandler(handler)
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = logging.StreamHandler()
    handler.setFormatter(fmt)
    flask_app.logger.addHandler(handler)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_by_name[config_name])
    configure_logging(flask_app)

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    jwt.init_app(flask_app)
    # Rate limiting: use Redis only if explicitly set, otherwise in-memory (no Redis required)
    storage_uri = flask_app.config.get("RATELIMIT_STORAGE_URI") or flask_app.config.get("REDIS_URL") or "memory://"
    flask_app.config["RATELIMIT_STORAGE_URI"] = storage_uri
    limiter.init_app(flask_app)
    cors_origins = [o.strip() for o in flask_app.config["CORS_ORIGINS"].split(",") if o.strip()]
    CORS(flask_app, origins=cors_origins, supports_credentials=True)

    from app.routes import register_blueprints
    register_blueprints(flask_app)

    @flask_app.before_request
    def log_request():
        g.current_user_name = None
        try:
            user_id = get_jwt_identity()
            if user_id:
                from app.models import User
                user = User.query.get(user_id)
                if user:
                    g.current_user_name = f"{user.first_name} {user.last_name}".strip()
        except Exception:
            g.current_user_name = None
        flask_app.logger.debug("Request: %s %s", request.method, request.path)

    @flask_app.after_request
    def log_response(response):
        flask_app.logger.info(
            "%s %s -> %s",
            request.method,
            request.path,
            response.status_code,
        )
        return response

    @flask_app.errorhandler(RateLimitExceeded)
    def rate_limited(e):
        flask_app.logger.warning("Rate limit exceeded: %s %s", request.method, request.path)
        msg = getattr(e, "description", None) or str(e) or "Too many requests. Please wait before trying again."
        return jsonify({"message": msg, "error": "rate_limit_exceeded"}), 429

    @flask_app.errorhandler(400)
    def bad_request(e):
        flask_app.logger.warning("Bad request: %s", e)
        return jsonify({"message": str(e) or "Bad request", "error": "bad_request"}), 400

    @flask_app.errorhandler(403)
    def forbidden(e):
        flask_app.logger.warning("Forbidden: %s %s - %s", request.method, request.path, e)
        return jsonify({"message": str(e) or "Forbidden", "error": "forbidden"}), 403

    @flask_app.errorhandler(404)
    def not_found(e):
        flask_app.logger.info("Not found: %s %s", request.method, request.path)
        return jsonify({"message": str(e) or "Not found", "error": "not_found"}), 404

    @flask_app.errorhandler(500)
    def internal_error(e):
        flask_app.logger.exception("Internal server error: %s", e)
        return jsonify({"message": "Internal server error", "error": "internal_error"}), 500

    with flask_app.app_context():
        import app.models  # noqa: F401 - register models for migrations

    make_celery_extension(flask_app)
    flask_app.logger.info("Application created (env=%s)", config_name)
    return flask_app
