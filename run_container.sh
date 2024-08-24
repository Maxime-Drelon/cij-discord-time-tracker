#!/bin/bash

# Variables
IMAGE_NAME="cij-discord-time-tracker"
CONTAINER_NAME="cij-discord-time-tracker-container"

# Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Run the Docker container
echo "Running Docker container..."
docker run -d --name $CONTAINER_NAME $IMAGE_NAME

echo "Container is running with name: $CONTAINER_NAME"
