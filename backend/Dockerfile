# Use an official Python image as the base image
FROM python:3.12-slim-bullseye

# Set environment variables (don't write .pyc files, and display output in real time)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for psycopg2 and any necessary build tools, and clean up
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy only the dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# App code mounting, port setup and starting command is in docker-compose
