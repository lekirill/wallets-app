Wallets app (Django + MySQL + Redis)
================

**Run (first db, then app and cache)**
```sh
docker-compose up -d --build db
docker-compose up -d --build
```

Wallet API runs on:
```
http://0.0.0.0:8080/
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