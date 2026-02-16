# Use a newer Python runtime that supports accelerate 1.12.0
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY ShopifySentinel/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ShopifySentinel/ /app/ShopifySentinel/

# The command to run the application
CMD ["python", "ShopifySentinel/main.py"]