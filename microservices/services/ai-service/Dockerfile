FROM python:3.10-slim

# Install development tools
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Set up the directory structure to match local development
WORKDIR /app/microservices

# Copy requirements from the main project (build context is backend root)
COPY microservices/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development dependencies
RUN pip install --no-cache-dir ipdb debugpy

# Copy shared utilities to match local structure (build context is backend root)
COPY microservices/shared ./shared

# Copy service code to match local structure (build context is backend root)
COPY microservices/services/ai-service ./services/ai-service

# Set working directory to the service source directory (matching local development)
WORKDIR /app/microservices/services/ai-service/src

# Expose port for FastAPI
EXPOSE 8000

# Expose port for debugger
EXPOSE 5678

CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
