from app import db
from app.models import ExpenseCategory


def list_expense_categories(organisation_id):
    return ExpenseCategory.query.filter_by(organisation_id=organisation_id).order_by(ExpenseCategory.name).all()


def create_expense_category(organisation_id, data):
    category = ExpenseCategory(
        organisation_id=organisation_id,
        name=data["name"],
    )
    db.session.add(category)
    db.session.commit()
    return category


def get_expense_category(organisation_id, category_id):
    return ExpenseCategory.query.filter_by(id=category_id, organisation_id=organisation_id).first()


def update_expense_category(category, data):
    if "name" in data:
        category.name = data["name"]
    db.session.commit()
    return category


def delete_expense_category(category):
    db.session.delete(category)
    db.session.commit()
