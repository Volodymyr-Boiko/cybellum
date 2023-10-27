FROM python:3.11

WORKDIR /app

ENV POETRY_VERSION=1.1.11 \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:${PATH}" \
    PYTHONPATH="${PYTHONPATH}:/app"

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    curl -sSL https://install.python-poetry.org | python - && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN poetry install --no-interaction --no-ansi
