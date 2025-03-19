# Use an official Node image as the base image
FROM node:22-alpine

# Set environment variables (helps hot-reloading and disables telemetry)
ENV WATCHPACK_POLLING true
ENV NEXT_TELEMETRY_DISABLED 1

# Set the working directory in the container
WORKDIR /app

# Copy only the dependency list
COPY package*.json .

# Install dependencies
RUN npm install

# App code mounting, port setup and starting command is in docker-compose
