"""
Seed dummy data: Organisation FAIMOUS SARL and user N'faly Kaba.
Run from backend/ with venv activated: python seed_dummy.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# run.py loads .env; importing app creates the Flask app
from run import app
from app import db
from app.models import Organisation, User


def seed():
    with app.app_context():
        # Get or create organisation
        org = Organisation.query.filter_by(name="FAIMOUS SARL").first()
        if org:
            print("Organisation FAIMOUS SARL already exists, using it.")
        else:
            org = Organisation(
                name="FAIMOUS SARL",
                currency_default="GNF",
                language_default="fr",
            )
            db.session.add(org)
            db.session.flush()
            print("Created organisation FAIMOUS SARL.")

        user = User.query.filter_by(email="kabanfaly@hotmail.com").first()
        if user:
            user.organisation_id = org.id
            user.role = "admin"
            user.activated = True
            db.session.commit()
            print("User kabanfaly@hotmail.com already exists; associated to FAIMOUS SARL and set role to admin.")
        else:
            user = User(
                organisation_id=org.id,
                first_name="N'faly",
                last_name="Kaba",
                email="kabanfaly@hotmail.com",
                role="admin",
                language="fr",
                activated=True,
            )
            user.set_password("Motdepasse123!")
            db.session.add(user)
            db.session.commit()
            print("Created user N'faly Kaba (kabanfaly@hotmail.com) with role admin.")


if __name__ == "__main__":
    seed()
