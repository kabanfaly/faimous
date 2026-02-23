from datetime import datetime
from flask import g, has_request_context
from sqlalchemy import event
from sqlalchemy.orm import Mapper

from app import db


class AuditMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)


def _get_actor_name():
    if not has_request_context():
        return None
    actor = getattr(g, "current_user_name", None)
    return actor or None


@event.listens_for(Mapper, "before_insert")
def _set_audit_fields(mapper, connection, target):
    if not isinstance(target, AuditMixin):
        return
    actor = _get_actor_name()
    if actor:
        if not getattr(target, "created_by", None):
            target.created_by = actor
        target.updated_by = actor


@event.listens_for(Mapper, "before_update")
def _set_audit_updated_by(mapper, connection, target):
    if not isinstance(target, AuditMixin):
        return
    actor = _get_actor_name()
    if actor:
        target.updated_by = actor
