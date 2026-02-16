# Use a newer Python runtime
FROM python:3.10-slim

# Install system dependencies required for some python packages to build
RUN apt-get update && apt-get install -y \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install requirements
COPY ShopifySentinel/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY ShopifySentinel/ /app/ShopifySentinel/

CMD ["python", "ShopifySentinel/main.py"]