# sparkly
Example FastAPI project

The goal of this project is to implement simple API to retrieve Vehicle information.

Main technologies/libraries:
* Python 3.10.4
* FastAPI
* SQLAlchemy
* Pytest
* Postgresql

Tools to enforce code guidelines:
* [black](https://github.com/psf/black)
* [flakeheaven](https://github.com/flakeheaven/flakeheaven)
* [mypy](https://github.com/python/mypy)
* [isort](https://github.com/PyCQA/isort)
* [precommit](https://pre-commit.com/)

# Development

Start from installing poetry

```bash
pip install poetry
```

Installing dependency

```bash
poetry install
```

Activating precommit

```bash
pre-commit install
```

To start the application

```bash
# Create your own settings
cp env.example .env

# Start database
docker-compose up -d postgres

# Apply migrations (ensure that database is already started)
alembic upgrade heads

# Load example data
# When asked to enter path, press enter
poe load-data

# Setup and build application
docker-compose up --build app
```

Go to `http://localhost:8000/docs` to see available endpoints.

To execute tests

```bash
poe test
```

# Information

## Functionality:

- [x] Create Vehicle
- [x] Create Vehicle Log
- [x] Get Vehicle Logs by Vehicle ID
- [x] List Vehicles
- [x] Load Vehicle Logs from CSV
- [ ] Filter Logs by timestamp

## To be done:

- [ ] Add Cassandra database support
- [ ] Add endpoint validation
- [ ] Add more tests
- [x] Cleanup resources after tests
