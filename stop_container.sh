#!/bin/bash

# Variables
CONTAINER_NAME="cij-discord-time-tracker-container"

# Stop the Docker container
echo "Stopping Docker container..."
docker stop $CONTAINER_NAME

# Remove the Docker container
echo "Removing Docker container..."
docker rm $CONTAINER_NAME

echo "Container $CONTAINER_NAME has been stopped and removed."
