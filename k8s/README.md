# Career Advisor Kubernetes Deployment

This directory contains Kubernetes manifests and deployment scripts for running the Career Advisor microservices locally using minikube or kind.

## Prerequisites

1. **Docker** - For building container images
2. **kubectl** - Kubernetes command-line tool
3. **minikube** OR **kind** - Local Kubernetes cluster

### Install Prerequisites (macOS)

```bash
# Install Docker Desktop (includes kubectl)
# Download from: https://www.docker.com/products/docker-desktop

# Install minikube
brew install minikube

# OR install kind
brew install kind

# Install nginx ingress controller (for minikube)
minikube addons enable ingress
```

## Quick Start

### Option 1: Using Minikube

```bash
# 1. Start minikube cluster
minikube start

# 2. Enable ingress addon
minikube addons enable ingress

# 3. Deploy Career Advisor
cd k8s/
chmod +x *.sh
./deploy.sh

# 4. Add to /etc/hosts for local access
echo "$(minikube ip) career-advisor.local" | sudo tee -a /etc/hosts

# 5. Test the deployment
curl http://career-advisor.local/api/prompts
```

### Option 2: Using Kind

```bash
# 1. Create kind cluster
kind create cluster --name career-advisor

# 2. Install nginx ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# 3. Wait for ingress controller
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

# 4. Deploy Career Advisor
cd k8s/
chmod +x *.sh
./deploy.sh

# 5. Port forward for local access
kubectl port-forward -n career-advisor svc/users-service 8001:8000 &
kubectl port-forward -n career-advisor svc/conversations-service 8002:8000 &
kubectl port-forward -n career-advisor svc/messages-service 8003:8000 &
kubectl port-forward -n career-advisor svc/prompts-service 8004:8000 &
kubectl port-forward -n career-advisor svc/llm-service 8005:8000 &
```

## Architecture

The Kubernetes deployment includes:

- **Namespace**: `career-advisor` - Isolates all resources
- **ConfigMap**: Shared configuration for all services
- **Secret**: PostgreSQL credentials
- **StatefulSet**: PostgreSQL database with persistent storage
- **Deployments**: 5 microservices (users, conversations, messages, prompts, llm)
- **Services**: ClusterIP services for internal communication
- **Ingress**: Nginx ingress for external API access

### Service Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Nginx Ingress │────│  Load Balancer  │
└─────────────────┘    └─────────────────┘
         │                       │
         ├───────────────────────┼─────────────────────┐
         │                       │                     │
┌────────▼────────┐    ┌─────────▼──────┐    ┌────────▼────────┐
│  Users Service  │    │ Conversations  │    │ Messages Service│
│   (Port 8000)   │    │    Service     │    │   (Port 8000)   │
└─────────────────┘    │  (Port 8000)   │    └─────────────────┘
                       └────────────────┘
         │                       │                     │
         └───────────────────────┼─────────────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │    PostgreSQL DB         │
                    │   (StatefulSet)          │
                    └──────────────────────────┘
```

## Files Overview

- `namespace.yaml` - Creates the career-advisor namespace
- `configmap.yaml` - Shared configuration for all services
- `postgres.yaml` - PostgreSQL database (StatefulSet + Service + Secret)
- `*-service.yaml` - Individual microservice deployments and services
- `ingress.yaml` - Nginx ingress controller configuration
- `build-images.sh` - Script to build all Docker images
- `deploy.sh` - Complete deployment script
- `cleanup.sh` - Remove all resources

## Manual Deployment Steps

If you prefer to deploy manually:

```bash
# 1. Build images
./build-images.sh

# 2. Apply manifests in order
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f postgres.yaml

# Wait for PostgreSQL
kubectl wait --for=condition=ready pod -l app=postgres -n career-advisor --timeout=300s

# 3. Deploy services
kubectl apply -f users-service.yaml
kubectl apply -f conversations-service.yaml
kubectl apply -f messages-service.yaml
kubectl apply -f prompts-service.yaml
kubectl apply -f llm-service.yaml

# 4. Apply ingress
kubectl apply -f ingress.yaml
```

## Monitoring and Debugging

```bash
# Check pod status
kubectl get pods -n career-advisor

# Check service status
kubectl get services -n career-advisor

# View logs for a specific service
kubectl logs -f deployment/users-service -n career-advisor

# Describe a pod for troubleshooting
kubectl describe pod <pod-name> -n career-advisor

# Execute into a pod
kubectl exec -it <pod-name> -n career-advisor -- /bin/bash

# Check ingress status
kubectl get ingress -n career-advisor
```

## Scaling Services

```bash
# Scale a specific service
kubectl scale deployment users-service --replicas=3 -n career-advisor

# Scale all services
kubectl scale deployment --all --replicas=2 -n career-advisor
```

## Database Access

```bash
# Port forward to PostgreSQL
kubectl port-forward -n career-advisor svc/postgres-service 5432:5432

# Connect using psql (in another terminal)
psql -h localhost -U postgres -d career_advisor
```

## API Testing

Once deployed, test the APIs:

```bash
# Test prompts service
curl http://career-advisor.local/api/prompts

# Test users service
curl http://career-advisor.local/api/users

# Or using port-forward (kind)
curl http://localhost:8004/prompts
```

## Cleanup

To remove all resources:

```bash
./cleanup.sh

# Or manually
kubectl delete namespace career-advisor
```

## Troubleshooting

### Common Issues

1. **Images not found**: Ensure images are built and loaded into minikube
   ```bash
   minikube image ls | grep career-advisor
   ```

2. **Ingress not working**: Check if ingress controller is running
   ```bash
   kubectl get pods -n ingress-nginx
   ```

3. **Database connection issues**: Check PostgreSQL pod logs
   ```bash
   kubectl logs -f statefulset/postgres -n career-advisor
   ```

4. **Service startup failures**: Check individual service logs
   ```bash
   kubectl logs -f deployment/users-service -n career-advisor
   ```

### Resource Requirements

- **Minimum**: 4GB RAM, 2 CPU cores
- **Recommended**: 8GB RAM, 4 CPU cores

### Performance Tuning

- Adjust resource requests/limits in deployment files
- Scale replicas based on load
- Use horizontal pod autoscaling for production
