# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY ShopifySentinel/requirements.txt .
# Note: The requirements.txt file contains local file dependencies ("file:///...").
# These will cause the build to fail. You need to replace them with
# packages from PyPI or another accessible package repository.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ShopifySentinel/ /app/ShopifySentinel/

# The command to run the application
CMD ["python", "ShopifySentinel/main.py"]
