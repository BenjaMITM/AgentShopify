# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY ShopifySentinel/requirements.txt .
# Note: The requirements.txt file has been cleaned of local file dependencies.
# However, it may still be missing some packages that were referenced via
# local paths. If the build fails due to missing packages, you may need to
# add them to requirements.txt manually.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ShopifySentinel/ /app/ShopifySentinel/

# The command to run the application
CMD ["python", "ShopifySentinel/main.py"]
