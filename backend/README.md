## Backend (Django + DRF)

### Setup
1. Create env file:
```
cp .env.example .env
```
2. Create venv and install:
```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
3. Run migrations (requires Postgres running):
```
python manage.py migrate
```
4. Run server:
```
python manage.py runserver
```

### Notes
- Settings read from `.env` with `python-dotenv`.
- Database defaults to Postgres via env vars.

