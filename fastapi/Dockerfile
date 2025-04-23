FROM python:3.13-slim

# Install dependencies for psycopg2 and clean up
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Note: App code mounting, port setup, and starting command are handled in docker-compose
