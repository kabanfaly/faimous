# Faimous Backend

## Migrations

Run migrations **from this directory** (`backend/`) so Flask finds the app and the `db` command:

```bash
cd backend
flask db upgrade
```

Create a new revision:

```bash
cd backend
flask db revision -m "description"
```
