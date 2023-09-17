Wallets app (Django + MySQL + Redis)
================

**Run**
```sh
docker-compose up -d --build
```

**Run tests**
1. Workdir `./app/`
2. Set env **DEBUG** as `True`, **DJANGO_SETTINGS_MODULE** as `tests.settings`, **PYTHONUNBUFFERED** `True`
3. Copy local.json.example to local.json and set db parameters as in point 2
4. Run:
```sh
pip install coverage
coverage run manage.py test
coverage report
```