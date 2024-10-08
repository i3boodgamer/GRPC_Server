FROM ubuntu:24.04

# Установка нужных пакетов с удалением ненужных файлов после
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    postgresql \
    postgresql-contrib \
    curl \
    build-essential \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove build-essential python3-dev

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    rm -rf /var/cache/apt/archives/*

# Настройка окружения
ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Настройка рабочего каталога
WORKDIR /grpctz

# Копирование зависимостей и кода
COPY pyproject.toml poetry.lock ./
COPY server ./server
COPY client ./client
COPY proto ./proto
COPY core ./core
COPY alembic ./alembic
COPY utils ./utils
COPY .env ./
COPY init_db.sql ./

# Установка зависимостей через Poetry
RUN /root/.local/bin/poetry install --no-dev --no-interaction --no-ansi

# Запуск сервера и клиента
CMD poetry run python3 server/server.py & poetry run python3 client/client.py