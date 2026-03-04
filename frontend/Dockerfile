FROM python:3.11-slim

WORKDIR /app

# Copy frontend files
COPY public/ ./public/
COPY server.py .

# Expose port (Railway will use PORT env var)
EXPOSE 3000

# Run the server
CMD ["python", "server.py"]
