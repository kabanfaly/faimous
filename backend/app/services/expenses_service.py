from app import db
from app.models import Expense, ExpenseCategory


def get_organisation_id():
    from app.multi_tenant.context import get_current_organisation_id
    return get_current_organisation_id()


def list_expense_categories(organisation_id):
    return ExpenseCategory.query.filter_by(organisation_id=organisation_id).order_by(ExpenseCategory.name).all()


def create_expense_category(organisation_id, data):
    cat = ExpenseCategory(organisation_id=organisation_id, name=data["name"])
    db.session.add(cat)
    db.session.commit()
    return cat


def list_expenses(organisation_id):
    return Expense.query.filter_by(organisation_id=organisation_id).order_by(Expense.date.desc()).all()


def create_expense(organisation_id, data):
    expense = Expense(
        organisation_id=organisation_id,
        date=data["date"],
        description=data.get("description"),
        category_id=data.get("category_id"),
        amount=data["amount"],
        currency=data.get("currency"),
        amount_base=data.get("amount_base"),
        invoice_file=data.get("invoice_file"),
        payment_method=data.get("payment_method"),
    )
    db.session.add(expense)
    db.session.commit()
    return expense


def get_expense(organisation_id, expense_id):
    return Expense.query.filter_by(id=expense_id, organisation_id=organisation_id).first()


def update_expense(expense, data):
    if "date" in data:
        expense.date = data["date"]
    if "description" in data:
        expense.description = data["description"]
    if "category_id" in data:
        expense.category_id = data["category_id"]
    if "amount" in data:
        expense.amount = data["amount"]
    if "currency" in data:
        expense.currency = data["currency"]
    if "amount_base" in data:
        expense.amount_base = data["amount_base"]
    db.session.commit()
    return expense


def delete_expense(expense):
    db.session.delete(expense)
    db.session.commit()
