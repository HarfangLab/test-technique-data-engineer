FROM python:3.10

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY database/ ./database

RUN poetry install

COPY populate.py malware_families.py ./

ENTRYPOINT ["poetry", "run", "python", "-u", "populate.py"]