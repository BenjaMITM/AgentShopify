FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY ShopifySentinel /app/ShopifySentinel

# Keep Cloud Run runtime aligned with Agent Engine dependencies.
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r /app/ShopifySentinel/requirements.txt

EXPOSE 8080

# ADK API server is the documented production runtime for container deployments.
CMD ["sh", "-c", "adk api_server /app --host 0.0.0.0 --port ${PORT:-8080}"]
