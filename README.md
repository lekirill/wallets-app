Wallets app (Django + MySQL + Redis)
================

**Run (first db, the app and cache)**
```sh
docker-compose up -d --build db
docker-compose up -d --build
```

**Run tests**
1. Workdir `./app/`
2. Set env **DEBUG** as `True`, **DJANGO_SETTINGS_MODULE** as `tests.settings`, **PYTHONUNBUFFERED** `True`
3. Run:
```sh
pip install coverage
coverage run manage.py test
coverage report
```