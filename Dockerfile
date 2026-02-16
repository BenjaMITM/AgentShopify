FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY ShopifySentinel /app/ShopifySentinel

# ADK runtime required by ShopifySentinel/agent.py imports.
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir google-adk

EXPOSE 8080

# ADK API server is the documented production runtime for container deployments.
CMD ["sh", "-c", "adk api_server /app --host 0.0.0.0 --port ${PORT:-8080}"]
