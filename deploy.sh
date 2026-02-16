#!/usr/bin/env bash
set -euo pipefail

MODE="agent-engine"
PROJECT_ID="${GCLOUD_PROJECT:-}"
REGION="${GCLOUD_REGION:-us-central1}"
SERVICE_NAME="shopify-sentinel"
AGENT_DIR="ShopifySentinel"
STAGING_BUCKET="${STAGING_BUCKET:-}"
ARTIFACT_REPO="agent-images"
IMAGE_NAME="shopify-sentinel"
IMAGE_TAG="$(date +%Y%m%d-%H%M%S)"
ALLOW_UNAUTHENTICATED="false"

usage() {
  cat <<'USAGE'
Usage:
  ./deploy.sh [options]

Modes:
  --mode agent-engine   Deploy with ADK to Vertex AI Agent Engine (default)
  --mode cloud-run      Build + push image, then deploy to Cloud Run
  --mode push-only      Build + push image only

Options:
  --project ID          Google Cloud project ID (or set GCLOUD_PROJECT)
  --region REGION       Google Cloud region (default: us-central1)
  --service NAME        Cloud Run service name (default: shopify-sentinel)
  --agent-dir PATH      ADK agent directory (default: ShopifySentinel)
  --staging-bucket URI  GCS bucket for adk deploy agent_engine
  --repo NAME           Artifact Registry repo (default: agent-images)
  --image NAME          Container image name (default: shopify-sentinel)
  --tag TAG             Container image tag (default: timestamp)
  --allow-unauthenticated true|false (Cloud Run only; default: false)
  -h, --help            Show this help message
USAGE
}

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Error: required command not found: $cmd" >&2
    exit 1
  fi
}

load_agent_env() {
  local env_file="${AGENT_DIR}/.env"
  if [[ -f "$env_file" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$env_file"
    set +a
  fi
}

validate_optional_mcp_urls() {
  local vars=(
    "SHOPIFY_SENTINEL_MCP_GSC_URL"
    "SHOPIFY_SENTINEL_MCP_GA_URL"
    "SHOPIFY_SENTINEL_MCP_LIGHTHOUSE_URL"
    "SHOPIFY_SENTINEL_MCP_PLAYWRIGHT_URL"
    "SHOPIFY_SENTINEL_MCP_SHOPIFY_ADMIN_URL"
  )
  local var
  local url
  local http_code
  for var in "${vars[@]}"; do
    url="${!var:-}"
    if [[ -n "$url" ]]; then
      require_cmd curl
      http_code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 15 "$url" || true)"
      if [[ "$http_code" == "000" ]]; then
        echo "Error: ${var} is not reachable: ${url}" >&2
        exit 1
      fi
    fi
  done
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      MODE="$2"
      shift 2
      ;;
    --project)
      PROJECT_ID="$2"
      shift 2
      ;;
    --region)
      REGION="$2"
      shift 2
      ;;
    --service)
      SERVICE_NAME="$2"
      shift 2
      ;;
    --agent-dir)
      AGENT_DIR="$2"
      shift 2
      ;;
    --staging-bucket)
      STAGING_BUCKET="$2"
      shift 2
      ;;
    --repo)
      ARTIFACT_REPO="$2"
      shift 2
      ;;
    --image)
      IMAGE_NAME="$2"
      shift 2
      ;;
    --tag)
      IMAGE_TAG="$2"
      shift 2
      ;;
    --allow-unauthenticated)
      ALLOW_UNAUTHENTICATED="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Error: unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$PROJECT_ID" ]]; then
  read -r -p "Google Cloud project ID: " PROJECT_ID
fi

require_cmd gcloud
gcloud config set project "$PROJECT_ID" >/dev/null
load_agent_env

case "$MODE" in
  agent-engine)
    require_cmd adk
    require_cmd python

    if [[ -z "$STAGING_BUCKET" ]]; then
      read -r -p "GCS staging bucket (name or gs:// URI): " STAGING_BUCKET
    fi

    if [[ "$STAGING_BUCKET" != gs://* ]]; then
      STAGING_BUCKET="gs://${STAGING_BUCKET}"
    fi

    export GOOGLE_GENAI_USE_VERTEXAI=1
    export GOOGLE_CLOUD_PROJECT="$PROJECT_ID"
    export GOOGLE_CLOUD_LOCATION="$REGION"

    gcloud services enable aiplatform.googleapis.com storage.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com >/dev/null

    if ! gcloud storage buckets describe "$STAGING_BUCKET" >/dev/null 2>&1; then
      echo "Creating staging bucket: $STAGING_BUCKET"
      gcloud storage buckets create "$STAGING_BUCKET" --location="$REGION"
    fi

    echo "Running local syntax preflight for ${AGENT_DIR}..."
    python -m compileall -q "$AGENT_DIR"
    validate_optional_mcp_urls

    echo "Deploying ADK agent to Vertex AI Agent Engine..."
    adk deploy agent_engine "$AGENT_DIR" \
      --project "$PROJECT_ID" \
      --region "$REGION" \
      --staging_bucket "$STAGING_BUCKET"
    ;;

  cloud-run|push-only)
    gcloud services enable artifactregistry.googleapis.com run.googleapis.com cloudbuild.googleapis.com >/dev/null

    if ! gcloud artifacts repositories describe "$ARTIFACT_REPO" --location "$REGION" >/dev/null 2>&1; then
      echo "Creating Artifact Registry repository '$ARTIFACT_REPO' in '$REGION'..."
      gcloud artifacts repositories create "$ARTIFACT_REPO" \
        --repository-format docker \
        --location "$REGION" \
        --description "Container images for Shopify Sentinel"
    fi

    gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet

    IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${ARTIFACT_REPO}/${IMAGE_NAME}:${IMAGE_TAG}"

    echo "Building and pushing image with Cloud Build: $IMAGE_URI"
    # Build in Cloud Build to avoid local architecture mismatches (e.g. arm64 images from Apple Silicon).
    gcloud builds submit --tag "$IMAGE_URI" .

    if [[ "$MODE" == "cloud-run" ]]; then
      echo "Deploying to Cloud Run service: $SERVICE_NAME"

      if [[ "$ALLOW_UNAUTHENTICATED" == "true" ]]; then
        AUTH_FLAG="--allow-unauthenticated"
      else
        AUTH_FLAG="--no-allow-unauthenticated"
      fi

      ENV_VARS=(
        "GOOGLE_CLOUD_PROJECT=${PROJECT_ID}"
        "GOOGLE_CLOUD_LOCATION=${REGION}"
        "GOOGLE_GENAI_USE_VERTEXAI=TRUE"
      )
      MCP_ENV_KEYS=(
        "SHOPIFY_SENTINEL_MCP_GSC_URL"
        "SHOPIFY_SENTINEL_MCP_GA_URL"
        "SHOPIFY_SENTINEL_MCP_LIGHTHOUSE_URL"
        "SHOPIFY_SENTINEL_MCP_PLAYWRIGHT_URL"
        "SHOPIFY_SENTINEL_MCP_SHOPIFY_ADMIN_URL"
      )
      for key in "${MCP_ENV_KEYS[@]}"; do
        if [[ -n "${!key:-}" ]]; then
          ENV_VARS+=("${key}=${!key}")
        fi
      done
      ENV_VARS_CSV="$(IFS=,; echo "${ENV_VARS[*]}")"

      gcloud run deploy "$SERVICE_NAME" \
        --image "$IMAGE_URI" \
        --region "$REGION" \
        --platform managed \
        --port 8080 \
        --set-env-vars "$ENV_VARS_CSV" \
        "$AUTH_FLAG"
    else
      echo "Image pushed successfully: $IMAGE_URI"
    fi
    ;;

  *)
    echo "Error: invalid mode '$MODE'. Use: agent-engine | cloud-run | push-only" >&2
    exit 1
    ;;
esac
