FROM python:3.10-slim

# Install development tools and PostgreSQL client
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set up the directory structure to match local development
WORKDIR /app/microservices

# Copy service-specific requirements
COPY microservices/services/conversations-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development dependencies
RUN pip install --no-cache-dir ipdb debugpy

# Copy shared utilities to match local structure (build context is backend root)
COPY microservices/shared ./shared

# Copy service code to match local structure (build context is backend root)
COPY microservices/services/conversations-service ./services/conversations-service

# Make the shared startup script executable
RUN chmod +x ./shared/start-service.sh

# Set working directory to the service directory for migrations
WORKDIR /app/microservices/services/conversations-service

# Expose port for FastAPI
EXPOSE 8000

# Expose port for debugger
EXPOSE 5678

# Run the shared startup script
CMD ["sh", "/app/microservices/shared/start-service.sh"]
