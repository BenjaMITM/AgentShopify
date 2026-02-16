#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Prompt for user-specific configuration
read -p "Enter your Google Cloud Project ID: " GCLOUD_PROJECT
read -p "Enter the Google Cloud region (e.g., us-central1): " GCLOUD_REGION
read -p "Enter a name for your service (e.g., shopify-sentinel): " SERVICE_NAME

# Set the project and region for gcloud
gcloud config set project $GCLOUD_PROJECT
gcloud config set run/region $GCLOUD_REGION

# Define the image name for Google Container Registry
IMAGE_NAME="gcr.io/$GCLOUD_PROJECT/$SERVICE_NAME"

echo "--------------------------------------------------"
echo "Building the Docker image..."
echo "This may take a while."
echo "NOTE: This step will likely fail if your requirements.txt contains local file paths ('file:///...')."
echo "Please update requirements.txt to use packages from PyPI or another accessible repository."
echo "--------------------------------------------------"

# Build the Docker image
docker build -t $IMAGE_NAME .

echo "--------------------------------------------------"
echo "Pushing the Docker image to Google Container Registry..."
echo "--------------------------------------------------"

# Push the image to GCR
docker push $IMAGE_NAME

echo "--------------------------------------------------"
echo "Deploying the service to Google Cloud Run..."
echo "This will be deployed as a worker service, not a web-facing application."
echo "--------------------------------------------------"

# Deploy to Cloud Run.
# --no-cpu-throttling is often useful for background workers
# that need consistent processing, not just when a request comes in.
# Since this is a worker, we don't expose any ports.
gcloud run deploy $SERVICE_NAME 
  --image $IMAGE_NAME 
  --platform managed 
  --no-cpu-throttling 
  --no-allow-unauthenticated

echo "--------------------------------------------------"
echo "Deployment complete."
echo "Your service '$SERVICE_NAME' is deployed to Cloud Run in region '$GCLOUD_REGION'."
echo "You can manage your service in the Google Cloud Console."
echo "--------------------------------------------------"

