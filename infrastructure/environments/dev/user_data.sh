#!/bin/bash

# Career Advisor Dev Environment Setup Script
# This script runs on EC2 instance boot to set up Docker and deploy services

set -e

# Update system
yum update -y

# Install Docker
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Install Git
yum install -y git

# Create application directory
mkdir -p /opt/career-advisor
cd /opt/career-advisor

# Clone the repository
git clone ${github_repo} .
git checkout ${branch}

# Navigate to backend directory
cd backend

# Create environment file for Docker Compose
cat > .env << EOF
# Database Configuration
DATABASE_URL=${database_url}

# Service URLs (internal Docker network)
USERS_SERVICE_URL=http://users-service:8000
CONVERSATIONS_SERVICE_URL=http://conversations-service:8000
MESSAGES_SERVICE_URL=http://messages-service:8000
PROMPTS_SERVICE_URL=http://prompts-service:8000
LLM_SERVICE_URL=http://llm-service:8000

# XAI API Configuration (placeholder)
XAI_API_KEY=test-key-not-used
XAI_BASE_URL=https://api.x.ai/v1
XAI_MODEL=grok-beta

# Python Configuration
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
EOF

# Create nginx configuration for reverse proxy
mkdir -p nginx
cat > nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream users_service {
        server users-service:8000;
    }
    
    upstream conversations_service {
        server conversations-service:8000;
    }
    
    upstream messages_service {
        server messages-service:8000;
    }
    
    upstream prompts_service {
        server prompts-service:8000;
    }
    
    upstream llm_service {
        server llm-service:8000;
    }

    server {
        listen 80;
        
        # Health check endpoint
        location /health {
            return 200 "OK\n";
            add_header Content-Type text/plain;
        }
        
        # Route to services
        location /api/users/ {
            proxy_pass http://users_service/api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location /api/conversations/ {
            proxy_pass http://conversations_service/api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location /api/messages/ {
            proxy_pass http://messages_service/api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location /api/prompts/ {
            proxy_pass http://prompts_service/api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location /api/llm/ {
            proxy_pass http://llm_service/api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        # Default route to prompts service for demo
        location / {
            proxy_pass http://prompts_service/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
EOF

# Create Docker Compose override for dev environment
cat > docker-compose.dev.yml << 'EOF'
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - users-service
      - conversations-service
      - messages-service
      - prompts-service
      - llm-service
    restart: unless-stopped

  users-service:
    build:
      context: .
      dockerfile: microservices/services/users-service/Dockerfile
    environment:
      - DATABASE_URL=$${DATABASE_URL}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  conversations-service:
    build:
      context: .
      dockerfile: microservices/services/conversations-service/Dockerfile
    environment:
      - DATABASE_URL=$${DATABASE_URL}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  messages-service:
    build:
      context: .
      dockerfile: microservices/services/messages-service/Dockerfile
    environment:
      - DATABASE_URL=$${DATABASE_URL}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  prompts-service:
    build:
      context: .
      dockerfile: microservices/services/prompts-service/Dockerfile
    environment:
      - DATABASE_URL=$${DATABASE_URL}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  llm-service:
    build:
      context: .
      dockerfile: microservices/services/llm-service/Dockerfile
    environment:
      - DATABASE_URL=$${DATABASE_URL}
      - XAI_API_KEY=$${XAI_API_KEY}
      - XAI_BASE_URL=$${XAI_BASE_URL}
      - XAI_MODEL=$${XAI_MODEL}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
EOF

# Build and start services
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up -d

# Create systemd service for auto-start on boot
cat > /etc/systemd/system/career-advisor.service << 'EOF'
[Unit]
Description=Career Advisor Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/career-advisor/backend
ExecStart=/usr/local/bin/docker-compose -f docker-compose.dev.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.dev.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
systemctl enable career-advisor.service

# Create log rotation for Docker logs
cat > /etc/logrotate.d/docker-containers << 'EOF'
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size=1M
    missingok
    delaycompress
    copytruncate
}
EOF

# Set up basic monitoring script
cat > /opt/career-advisor/monitor.sh << 'EOF'
#!/bin/bash
# Simple monitoring script for Career Advisor services

cd /opt/career-advisor/backend

echo "=== Career Advisor Service Status ==="
echo "Date: $(date)"
echo ""

echo "Docker Compose Status:"
docker-compose -f docker-compose.dev.yml ps

echo ""
echo "Service Health Checks:"
services=("users-service" "conversations-service" "messages-service" "prompts-service" "llm-service")

for service in "$${services[@]}"; do
    if curl -s -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ $service: Healthy"
    else
        echo "❌ $service: Unhealthy"
    fi
done

echo ""
echo "System Resources:"
echo "Memory: $(free -h | grep '^Mem:' | awk '{print $3 "/" $2}')"
echo "Disk: $(df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 " used)"}')"
echo "Load: $(uptime | awk -F'load average:' '{print $2}')"
EOF

chmod +x /opt/career-advisor/monitor.sh

# Add monitoring to crontab for ec2-user
echo "*/5 * * * * /opt/career-advisor/monitor.sh >> /var/log/career-advisor-monitor.log 2>&1" | crontab -u ec2-user -

# Create simple status page
mkdir -p /var/www/html
cat > /var/www/html/status.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Career Advisor - Dev Environment</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .service { margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .healthy { background-color: #d4edda; }
        .unhealthy { background-color: #f8d7da; }
    </style>
</head>
<body>
    <h1>Career Advisor - Development Environment</h1>
    <p>Welcome to the Career Advisor microservices development deployment!</p>
    
    <h2>Available Services</h2>
    <div class="service">
        <strong>Users Service:</strong> <a href="/api/users/docs" target="_blank">API Documentation</a>
    </div>
    <div class="service">
        <strong>Conversations Service:</strong> <a href="/api/conversations/docs" target="_blank">API Documentation</a>
    </div>
    <div class="service">
        <strong>Messages Service:</strong> <a href="/api/messages/docs" target="_blank">API Documentation</a>
    </div>
    <div class="service">
        <strong>Prompts Service:</strong> <a href="/api/prompts/docs" target="_blank">API Documentation</a>
    </div>
    <div class="service">
        <strong>LLM Service:</strong> <a href="/api/llm/docs" target="_blank">API Documentation</a>
    </div>
    
    <h2>Monitoring</h2>
    <p>Check service status: <code>sudo /opt/career-advisor/monitor.sh</code></p>
    <p>View logs: <code>cd /opt/career-advisor/backend && docker-compose -f docker-compose.dev.yml logs -f</code></p>
    
    <h2>Management Commands</h2>
    <ul>
        <li>Restart services: <code>sudo systemctl restart career-advisor</code></li>
        <li>Stop services: <code>sudo systemctl stop career-advisor</code></li>
        <li>View service status: <code>sudo systemctl status career-advisor</code></li>
    </ul>
</body>
</html>
EOF

# Log completion
echo "$(date): Career Advisor dev environment setup completed successfully" >> /var/log/user-data.log

# Final status check
sleep 30
/opt/career-advisor/monitor.sh >> /var/log/user-data.log 2>&1
