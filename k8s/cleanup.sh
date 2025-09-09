#!/bin/bash

# Cleanup Career Advisor Kubernetes deployment
# This script removes all Career Advisor resources from Kubernetes

set -e

echo "🧹 Cleaning up Career Advisor Kubernetes deployment..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed."
    exit 1
fi

# Check if namespace exists
if ! kubectl get namespace career-advisor &> /dev/null; then
    echo "ℹ️  Career Advisor namespace not found. Nothing to clean up."
    exit 0
fi

echo "🗑️  Removing all resources in career-advisor namespace..."

# Delete all resources in the namespace
kubectl delete ingress --all -n career-advisor
kubectl delete services --all -n career-advisor
kubectl delete deployments --all -n career-advisor
kubectl delete statefulsets --all -n career-advisor
kubectl delete configmaps --all -n career-advisor
kubectl delete secrets --all -n career-advisor
kubectl delete pvc --all -n career-advisor

# Delete the namespace
kubectl delete namespace career-advisor

echo "✅ Cleanup complete!"
echo "🐳 Docker images are still available. To remove them:"
echo "   docker rmi career-advisor/users-service:latest"
echo "   docker rmi career-advisor/conversations-service:latest"
echo "   docker rmi career-advisor/messages-service:latest"
echo "   docker rmi career-advisor/prompts-service:latest"
echo "   docker rmi career-advisor/llm-service:latest"
