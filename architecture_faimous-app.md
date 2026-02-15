# 🐔 Faimous — Architecture SaaS complète

## Stack
- Backend: Python Flask (REST API)
- Frontend: Vue 3 + Vite
- DB: PostgreSQL
- Cache/Queue: Redis + Celery
- Charts: Chart.js / ECharts
- Auth: JWT
- PDF: ReportLab
- Container: Docker

---

# 1. Architecture SaaS Multi‑tenant

## Organisation (Tenant)
Chaque client = une organisation.
Toutes les tables métiers contiennent `organisation_id`.

### organisations
- id
- name
- currency_default
- language_default
- created_at

---

# 2. Multi‑fermes

### farms
- id
- organisation_id
- name
- location

---

# 3. Multi‑devises

### currencies
- code (GNF, XOF, CAD, USD, EUR)
- symbol

### exchange_rates
- from_currency
- to_currency
- rate
- date

Toutes les tables financières contiennent:
- currency
- amount
- amount_base

---

# 4. Multilingue
Frontend: Vue i18n
Langues: Français / English

---

# 5. Modules Fonctionnels

## Dashboard
- KPIs production
- Cashflow
- Alertes

## Production
- Pontes
- Casses
- Mortalité
- Cheptel

## Ventes
- Paiements partiels
- Reste à encaisser

## Achats
- Dette fournisseurs

## Stock
- Produits
- Mouvements
- Alertes rupture

## Dépenses
- Catégories
- Résultat

## Alimentation
- Préparations
- Consommation

## Financement
- Apports actionnaires

## Utilisateurs
- owner / admin / manager / worker

---

# 6. Modèle de Données

## Référentiels

### cities
- id
- name
- prefecture

### wholesalers
- id
- name
- city_id

### suppliers
- id
- name
- phone
- email
- city_id

### products
- id
- name
- description
- type
- unit

### expense_categories
- id
- name

### shareholders
- id
- first_name
- last_name
- phone
- email

---

## Production

### egg_productions
- id
- date
- eggs_count
- broken_count
- trays
- remaining
- note

### flock_records
- id
- date
- total_hens
- dead
- note

### daily_operations
- id
- date
- period
- collect1
- collect2
- collect3
- collect4
- broken
- hens
- dead

---

## Sales

### sales
- id
- date
- type
- quantity
- unit_price
- total_price
- theoretical_price
- price_diff
- wholesaler_id
- payment_status
- currency
- amount_base

### payments_received
- id
- sale_id
- date
- amount
- payment_method
- note

---

## Purchases

### purchases
- id
- date
- supplier_id
- product_id
- unit_price
- quantity
- total_price
- status
- currency
- amount_base

### supplier_payments
- id
- purchase_id
- date
- amount
- payment_method
- note

---

## Stock

### stock_movements
- id
- date
- product_id
- description
- quantity
- price
- movement_type
- purchase_id

---

## Expenses

### expenses
- id
- date
- description
- category_id
- amount
- currency
- amount_base
- invoice_file
- payment_method

---

## Feed

### feed_preparations
- id
- date
- quantity_kg
- ratio
- hens_available
- expected_end_date
- note

---

## Financing

### contributions
- id
- date
- shareholder_id
- amount
- currency
- amount_base
- description

---

## Users

### users
- id
- organisation_id
- first_name
- last_name
- gender
- email
- password
- language
- status
- role

---

# 7. KPIs Dashboard

## Production
- Pontes jour / semaine / mois
- Taux casse
- Poules actuelles
- Mortalité

## Finance
- CA
- Encaissé
- Reste à encaisser
- Reste à payer
- Résultat

## Stock
- Valeur stock
- Produits critiques

---

# 8. API

## Auth
- POST /auth/login
- POST /auth/register
- GET /me

## Organisation
- POST /organisations
- GET /organisations/current

## Production
- POST /production/eggs
- POST /production/flock
- GET /production/kpis

## Sales
- POST /sales
- POST /sales/payment
- GET /sales/unpaid

## Purchases
- POST /purchases
- POST /purchases/payment
- GET /purchases/unpaid

## Finance
- GET /finance/result
- GET /finance/cashflow

## Dashboard
- GET /dashboard/summary
- GET /dashboard/charts

---

# 9. Backend Structure

```
backend/
 ├── app/
 │   ├── models/
 │   ├── routes/
 │   ├── services/
 │   ├── schemas/
 │   ├── auth/
 │   ├── billing/
 │   ├── multi_tenant/
 │   └── dashboard/
 ├── migrations/
 ├── config.py
 └── run.py
```

---

# 10. Frontend Structure

```
src/
 ├── layouts/
 ├── views/
 ├── i18n/
 │   ├── fr.json
 │   └── en.json
 ├── store/
 ├── api/
 └── components/
```



---

**Fin — Architecture SaaS Application Aviculture**

