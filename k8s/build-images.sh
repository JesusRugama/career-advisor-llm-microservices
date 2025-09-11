#!/bin/bash

# Build Docker images for Kubernetes deployment
# This script builds all microservice images for local Kubernetes deployment

set -e

echo "🏗️  Building Docker images for Kubernetes deployment..."

# Set the build context to the backend root directory
cd "$(dirname "$0")/.."

# Build all microservice images
echo "📦 Building users-service..."
docker build -t career-advisor/users-service:latest -f microservices/services/users-service/Dockerfile .

echo "📦 Building conversations-service..."
docker build -t career-advisor/conversations-service:latest -f microservices/services/conversations-service/Dockerfile .

echo "📦 Building prompts-service..."
docker build -t career-advisor/prompts-service:latest -f microservices/services/prompts-service/Dockerfile .

echo "✅ All Docker images built successfully!"
echo ""
echo "📋 Built images:"
docker images | grep career-advisor
