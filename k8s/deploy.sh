#!/bin/bash

# Deploy Career Advisor microservices to local Kubernetes
# Prerequisites: minikube or kind cluster running, kubectl configured

set -e

echo "🚀 Deploying Career Advisor to Kubernetes..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if cluster is running
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ No Kubernetes cluster found. Please start minikube or kind cluster first."
    echo "   For minikube: minikube start"
    echo "   For kind: kind create cluster --name career-advisor"
    exit 1
fi

echo "✅ Kubernetes cluster detected"

# Build Docker images first
echo "🏗️  Building Docker images..."
./build-images.sh

# If using minikube, load images into minikube
if command -v minikube &> /dev/null && minikube status &> /dev/null; then
    echo "📥 Loading images into minikube..."
    minikube image load career-advisor/users-service:latest
    minikube image load career-advisor/conversations-service:latest
    minikube image load career-advisor/messages-service:latest
    minikube image load career-advisor/prompts-service:latest
    minikube image load career-advisor/llm-service:latest
fi

# Apply Kubernetes manifests in order
echo "📋 Applying Kubernetes manifests..."

echo "  → Creating namespace..."
kubectl apply -f namespace.yaml

echo "  → Creating ConfigMap..."
kubectl apply -f configmap.yaml

echo "  → Deploying PostgreSQL..."
kubectl apply -f postgres.yaml

echo "  → Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n career-advisor --timeout=300s

echo "  → Deploying microservices..."
kubectl apply -f users-service.yaml
kubectl apply -f conversations-service.yaml
kubectl apply -f messages-service.yaml
kubectl apply -f prompts-service.yaml
kubectl apply -f llm-service.yaml

echo "  → Waiting for services to be ready..."
kubectl wait --for=condition=available deployment --all -n career-advisor --timeout=300s

echo "  → Creating Ingress..."
kubectl apply -f ingress.yaml

echo "✅ Deployment complete!"
echo ""
echo "📊 Cluster status:"
kubectl get pods -n career-advisor
echo ""
kubectl get services -n career-advisor
echo ""
echo "🌐 Access the API:"
if command -v minikube &> /dev/null && minikube status &> /dev/null; then
    echo "   Add to /etc/hosts: $(minikube ip) career-advisor.local"
    echo "   Then access: http://career-advisor.local/api/prompts"
else
    echo "   Configure port-forward or ingress controller as needed"
    echo "   Example: kubectl port-forward -n career-advisor svc/users-service 8001:8000"
fi
