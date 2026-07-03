# ── Build stage ─────────────────────────────────────────────────────
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy dependency manifests
COPY pyproject.toml .

# Install dependencies directly into the system
RUN pip install --no-cache-dir \
    "fastapi>=0.110,<1.0" \
    "uvicorn[standard]>=0.29,<1.0" \
    "pydantic-settings>=2.2,<3.0" \
    "celery>=5.3,<6.0" \
    "redis>=5.0,<6.0"

# Copy application code
COPY app/ ./app/
COPY pyproject.toml .

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Default command (overridden in compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
