# Faimous — SaaS Aviculture

Application SaaS multi-tenant pour la gestion de fermes avicoles (production d’œufs, ventes, achats, stock, dépenses, alimentation, financement).

## Stack

- **Backend:** Python Flask (REST API), PostgreSQL, Celery, JWT, ReportLab (Redis optionnel)
- **Frontend:** Vue 3 + Vite, Vue i18n (fr/en), Chart.js

## Démarrage rapide

### Prérequis

- Python 3.11+
- PostgreSQL
- Node.js 18+ et npm (frontend)

### Backend (avec venv)

Le backend s’exécute dans un environnement virtuel Python (`venv`).

```bash
cd backend

# Créer le venv (une seule fois)
python3 -m venv venv

# Activer le venv
# Linux / macOS :
source venv/bin/activate
# Windows (PowerShell) :
# .\venv\Scripts\Activate.ps1
# Windows (cmd) :
# venv\Scripts\activate.bat

# Copier le fichier d’environnement et l’éditer
cp .env.example .env
# Éditer .env avec votre base PostgreSQL, secret JWT, etc.

# Installer les dépendances dans le venv
pip install -r requirements.txt

# Créer la base PostgreSQL puis appliquer les migrations
export FLASK_APP=run.py
python -m flask db upgrade

# Lancer l’API (avec le venv activé)
# Port 5001 pour éviter le conflit avec AirPlay Receiver sur macOS (port 5000)
python run.py
# ou : FLASK_RUN_PORT=5001 python -m flask run
```

L’API est disponible sur http://localhost:5001. Sur macOS, le port 5000 est souvent utilisé par AirPlay Receiver ; le backend utilise donc 5001 par défaut (variable `FLASK_PORT` ou `FLASK_RUN_PORT`).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Ouvrir http://localhost:5174 (ou 5173). L’API est proxifiée vers http://localhost:5001.

### Celery (optionnel)

Sans Redis, Celery utilise un broker en mémoire (développement). Avec le venv activé dans `backend/` :

```bash
cd backend
source venv/bin/activate   # si pas déjà activé
python -m celery -A celery_worker worker -l info
```

Pour utiliser Redis (broker partagé, limites de débit partagées), définir `REDIS_URL` dans `.env`.

## Fichier d’environnement (backend)

Le backend charge les variables depuis `backend/.env`. Copier `.env.example` vers `.env` et adapter :

| Variable | Description |
|----------|-------------|
| `FLASK_ENV` | `development` ou `production` |
| `FLASK_APP` | `run.py` |
| `SECRET_KEY` / `JWT_SECRET_KEY` | Secret pour sessions et JWT (à changer en production) |
| `SQLALCHEMY_DATABASE_URI` | URL de connexion PostgreSQL |
| `REDIS_URL` / `CELERY_BROKER_URL` | Optionnel. Si non défini : pas de Redis (Celery en mémoire, rate limit en mémoire). |

## Structure

- `backend/` — API Flask, modèles, services, migrations
- `frontend/` — Vue 3 + Vite, i18n, vues par module
- `architecture_faimous-app.md` — Spécification de l’architecture
