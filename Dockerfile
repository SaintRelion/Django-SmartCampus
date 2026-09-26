FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN --mount=type=secret,id=sr_django_legacy_token \
    TOKEN="$(cat /run/secrets/sr_django_legacy_token)" && \
    git config --global url."https://oauth2:${TOKEN}@github.com/".insteadOf "https://github.com/" && \
    uv sync --frozen --no-dev && \
    git config --global --unset-all url."https://oauth2:${TOKEN}@github.com/".insteadOf

COPY src/ ./

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000