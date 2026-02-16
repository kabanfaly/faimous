"""Supported currencies: symbols and display names."""

CURRENCY_SYMBOLS = {
    "USD": "$",
    "CAD": "C$",
    "EUR": "€",
    "GNF": "FG",
    "XOF": "CFA",
}

CURRENCY_NAMES = {
    "USD": "US Dollar",
    "CAD": "Canadian Dollar",
    "EUR": "Euro",
    "GNF": "Guinean Franc",
    "XOF": "West African CFA Franc",
}


def get_currencies_list():
    """Return list of { code, symbol, name } for all supported currencies."""
    return [
        {"code": code, "symbol": CURRENCY_SYMBOLS[code], "name": CURRENCY_NAMES[code]}
        for code in CURRENCY_SYMBOLS
    ]
