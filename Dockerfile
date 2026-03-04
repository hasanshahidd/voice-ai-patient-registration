# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire backend folder
COPY backend/ .

# Expose port (Railway will inject PORT env var)
EXPOSE 8000

# Start the FastAPI application
CMD uvicorn app:app --host 0.0.0.0 --port $PORT
