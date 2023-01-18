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
cp env.example .env
docker-compose up --build
```

Go to `http://localhost:8000/docs` to see available endpoints.

To load example data execute:

```bash
poe load-data
```

When asked to enter the path, press enter to load example data.
