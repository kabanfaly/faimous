from flask import g
from flask_jwt_extended import get_jwt


def get_current_organisation_id():
    """Return organisation_id from JWT claims. Set on g after JWT is verified."""
    if hasattr(g, "organisation_id"):
        return g.organisation_id
    try:
        claims = get_jwt()
        return claims.get("organisation_id")
    except Exception:
        return None


def set_current_organisation_id(organisation_id):
    """Set current organisation on request context (e.g. after JWT load)."""
    g.organisation_id = organisation_id
