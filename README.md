# ecommerce

## Installation

### Requirements

You have to have docker installed before to run this project easily.

### Steps

1. Run `docker-compose build`
2. Run `docker-compose run --rm --service-ports worker bash`
3. Inside the docker container terminal run `pytest -x` to run the application tests.
4. Enjoy it.
