#!/bin/bash

# Career Advisor Development Script with Skaffold
# This script provides fast development iteration with hot reloading

set -e

echo "🚀 Starting Career Advisor development environment with Skaffold..."

# Check if skaffold is available
if ! command -v skaffold &> /dev/null; then
    echo "❌ Skaffold is not installed. Installing now..."
    
    # Install Skaffold on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install skaffold
        else
            echo "Please install Homebrew first: https://brew.sh/"
            exit 1
        fi
    else
        echo "Please install Skaffold: https://skaffold.dev/docs/install/"
        exit 1
    fi
fi

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if cluster is running
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ No Kubernetes cluster found. Please start your cluster first."
    echo "   For minikube: minikube start"
    echo "   For kind: kind create cluster --name career-advisor"
    exit 1
fi

echo "✅ Kubernetes cluster detected"

# Start Skaffold development mode
echo "🔥 Starting Skaffold development mode with hot reloading..."
echo ""
echo "📋 What Skaffold will do:"
echo "  • Build all 5 microservice images with Docker"
echo "  • Deploy to your Kubernetes cluster"
echo "  • Set up port forwarding:"
echo "    - Users Service: http://localhost:8001"
echo "    - Conversations Service: http://localhost:8002"
echo "    - Messages Service: http://localhost:8003"
echo "    - Prompts Service: http://localhost:8004"
echo "    - LLM Service: http://localhost:8005"
echo "    - PostgreSQL: localhost:5432"
echo "  • Watch for file changes and sync automatically"
echo ""
echo "💡 To test: curl http://localhost:8004/prompts"
echo "💡 To stop: Press Ctrl+C"
echo ""

# Run Skaffold in development mode
skaffold dev --profile=dev --port-forward
