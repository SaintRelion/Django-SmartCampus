# syntax=docker/dockerfile:1.7

FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# requirements.txt contains a private GitHub dependency, so git is required.
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN --mount=type=secret,id=sr_django_legacy_token \
    SR_DJANGO_LEGACY_TOKEN="$(cat /run/secrets/sr_django_legacy_token)" \
    pip install \
        --no-cache-dir \
        --timeout 120 \
        --retries 10 \
        -r requirements.txt

COPY . .

EXPOSE 8000
