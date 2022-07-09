# Authentication with Flask, React, and Docker

https://testdriven.io/courses/auth-flask-react/

## Local

Creation

```bash
docker-compose up -d --build
```

Initialize

```bash
docker-compose exec api python manage.py recreate_db

docker-compose exec api python manage.py seed_db
```

Lint

```bash
docker-compose exec api flake8 src

docker-compose exec api black src

docker-compose exec api isort src
```

Test

```bash
docker-compose exec api python -m pytest "src/tests" -p no:warnings --cov="src"
```

Database

```bash
docker-compose exec api-db psql -U postgres
# \c api_dev
# select * from users;
```

## Remote
