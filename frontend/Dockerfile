FROM node:22-alpine

# Set environment variables (helps hot-reloading and disables telemetry)
ENV WATCHPACK_POLLING true
ENV NEXT_TELEMETRY_DISABLED 1

WORKDIR /app

COPY package*.json .

RUN npm install

# Note: App code mounting, port setup, and starting command are handled in docker-compose
