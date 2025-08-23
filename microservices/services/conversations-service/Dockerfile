FROM python:3.11-slim

WORKDIR /app

# Copy requirements from the main project
COPY ../../../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared utilities
COPY ../../shared /app/shared

# Copy service code
COPY src /app/src

WORKDIR /app/src

# Expose port
EXPOSE 8000

# Run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
