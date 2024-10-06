FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    postgresql \
    postgresql-contrib \
    curl \
    build-essential \
    python3-dev \
    && apt-get clean


RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /grpctz

COPY pyproject.toml poetry.lock ./
COPY server ./server
COPY client ./client
COPY proto ./proto
COPY core ./core
COPY alembic ./alembic
COPY utils ./utils
COPY .env ./
COPY init_db.sql ./



RUN /root/.local/bin/poetry install -vvv  # Для отладки

CMD poetry run python3 server/server.py & poetry run python3 client/client.py