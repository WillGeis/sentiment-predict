#!/bin/bash

IMAGE_NAME="stock-trader"
CONTAINER_NAME="stock-trader-container"
NETWORK_NAME="stock_network"

echo "Checking if Docker is running..."
if ! docker info >/dev/null 2>&1; then
    echo "Docker is not running. Please start Docker Desktop or the Docker daemon."
    exit 1
fi

echo "Building Docker image..."
docker build -t "$IMAGE_NAME" .

echo "Checking for existing container..."
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping and removing existing container..."
    docker stop "$CONTAINER_NAME"
    docker rm "$CONTAINER_NAME"
fi

echo "Ensuring network exists..."
if ! docker network ls | grep -q "$NETWORK_NAME"; then
    docker network create "$NETWORK_NAME"
fi

echo "Starting container..."
docker run -it --name "$CONTAINER_NAME" --network="$NETWORK_NAME" "$IMAGE_NAME"
