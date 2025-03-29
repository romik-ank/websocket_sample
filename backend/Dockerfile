FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    libgl1-mesa-glx \
    libssl-dev  # SSL support

RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy SSL certificates
COPY cert.pem /app/cert.pem
COPY key.pem /app/key.pem

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "/app/key.pem", "--ssl-certfile", "/app/cert.pem", "--reload"]