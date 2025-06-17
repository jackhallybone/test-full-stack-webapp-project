FROM python:3.12-slim-bullseye

# Install system dependencies for psycopg and clean up
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Note: App code mounting, port setup, and starting command are handled in docker-compose
