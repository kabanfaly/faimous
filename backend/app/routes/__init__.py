def register_blueprints(app):
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    # Others registered as we add them
    try:
        from app.routes.organisations import organisations_bp
        app.register_blueprint(organisations_bp, url_prefix="/api/organisations")
    except ImportError:
        pass
    try:
        from app.routes.production import production_bp
        app.register_blueprint(production_bp, url_prefix="/api/production")
    except ImportError:
        pass
    try:
        from app.routes.sales import sales_bp
        app.register_blueprint(sales_bp, url_prefix="/api/sales")
    except ImportError:
        pass
    try:
        from app.routes.purchases import purchases_bp
        app.register_blueprint(purchases_bp, url_prefix="/api/purchases")
    except ImportError:
        pass
    try:
        from app.routes.finance import finance_bp
        app.register_blueprint(finance_bp, url_prefix="/api/finance")
    except ImportError:
        pass
    try:
        from app.routes.dashboard import dashboard_bp
        app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    except ImportError:
        pass
    try:
        from app.routes.stock import stock_bp
        app.register_blueprint(stock_bp, url_prefix="/api/stock")
    except ImportError:
        pass
    try:
        from app.routes.expenses import expenses_bp
        app.register_blueprint(expenses_bp, url_prefix="/api/expenses")
    except ImportError:
        pass
    try:
        from app.routes.feed import feed_bp
        app.register_blueprint(feed_bp, url_prefix="/api/feed")
    except ImportError:
        pass
    try:
        from app.routes.contributions import contributions_bp
        app.register_blueprint(contributions_bp, url_prefix="/api/contributions")
    except ImportError:
        pass
    try:
        from app.routes.users import users_bp
        app.register_blueprint(users_bp, url_prefix="/api/users")
    except ImportError:
        pass
    try:
        from app.routes.suppliers import suppliers_bp
        app.register_blueprint(suppliers_bp, url_prefix="/api/suppliers")
    except ImportError:
        pass
    try:
        from app.routes.currencies import currencies_bp
        app.register_blueprint(currencies_bp, url_prefix="/api/currencies")
    except ImportError:
        pass
    try:
        from app.routes.cities import cities_bp
        app.register_blueprint(cities_bp, url_prefix="/api/cities")
    except ImportError:
        pass
    try:
        from app.routes.wholesalers import wholesalers_bp
        app.register_blueprint(wholesalers_bp, url_prefix="/api/wholesalers")
    except ImportError:
        pass
    try:
        from app.routes.products import products_bp
        app.register_blueprint(products_bp, url_prefix="/api/products")
    except ImportError:
        pass
    try:
        from app.routes.expense_categories import expense_categories_bp
        app.register_blueprint(expense_categories_bp, url_prefix="/api/expense-categories")
    except ImportError:
        pass
    try:
        from app.routes.shareholders import shareholders_bp
        app.register_blueprint(shareholders_bp, url_prefix="/api/shareholders")
    except ImportError:
        pass
    try:
        from app.routes.farms import farms_bp
        app.register_blueprint(farms_bp, url_prefix="/api/farms")
    except ImportError:
        pass
