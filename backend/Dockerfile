# Production Dockerfile for Railway (external DB like Neon)
FROM python:3.14-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package installation
RUN pip install --no-cache-dir uv

# Copy and install dependencies
COPY pyproject.toml ./
RUN uv pip install --system -r pyproject.toml

# Copy application code
COPY . .

# Create startup script
RUN echo '#!/bin/sh\n\
    set -e\n\
    echo "=== Running migrations ==="\n\
    alembic upgrade head\n\
    \n\
    if [ "$SEED" = "true" ]; then\n\
    echo "=== Seeding database ==="\n\
    python utils/seed_slack_template.py\n\
    python utils/seed_linear_template.py\n\
    python utils/seed_box_template.py\n\
    python utils/seed_tests.py\n\
    else\n\
    echo "=== Skipping seed (set SEED=true to enable) ==="\n\
    fi\n\
    \n\
    echo "=== Starting server ==="\n\
    exec uvicorn src.platform.api.main:app --host 0.0.0.0 --port ${PORT:-8000}\n\
    ' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]

