#!/usr/bin/env bash
set -euo pipefail

# Usage:
# ./build_and_run.sh [image_name] [tag]
# Example: ./build_and_run.sh py-payload-service fastapi:latest

IMAGE_NAME=${1:-py-payload-service}
IMAGE_TAG=${2:-latest}

FULL_TAG="${IMAGE_NAME}:${IMAGE_TAG}"

echo "Building ${FULL_TAG} using Dockerfile.prod..."
docker build -f Dockerfile.prod -t "${FULL_TAG}" .

echo "Built ${FULL_TAG}"

echo "Running container ${FULL_TAG} (detached) on port 8080 -> 8080"
docker run --rm -d -p 8080:8080 --name "${IMAGE_NAME//[:/]-}-runner" "${FULL_TAG}"

echo "Container started. Access the API at http://localhost:8080/docs"
