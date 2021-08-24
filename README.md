# ecommerce

## Installation

1. Create .env file and paste the following environment variables.
```
# Project (Project variables)
DB_NAME=ecommerce
DB_PASSWORD=ecommerce
DB_HOST=postgres
DB_PORT=5432

# Docker (Configuration for docker containers)
POSTGRES_DB=ecommerce
POSTGRES_USER=ecommerce
POSTGRES_PASSWORD=ecommerce
POSTGRES_PORT=5430
WORKER_PORT=8080

# Postgres Healthy (Healthy check to database availability)
DATABASE=postgres
```

2. Run in your terminal `docker-compose run --rm --service-ports worker bash`
3. Run in your docker terminal `python ecommerce/manage.py migrate`
4. Run in your docker terminal `python ecommerce/manage.py runserver 0:8000`

## Tests
1. Run in your terminal `docker-compose run --rm --service-ports worker bash`
2. Run in your docker terminal `cd ecommerce`
3. Run in your docker terminal `pytest -x`

## Documentation
We use swagger to generate the documentation to the rest api [documentation](http://localhost:8080/documentation/)
