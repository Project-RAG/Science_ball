# ── Build stage ─────────────────────────────────────────────────────
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Install build dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy dependency manifests
COPY pyproject.toml .

# Install dependencies into a temporary location
RUN pip install --no-cache-dir --target=/install \
    fastapi>=0.110,<1.0 \
    uvicorn[standard]>=0.29,<1.0 \
    pydantic-settings>=2.2,<3.0 \
    celery>=5.3,<6.0 \
    redis>=5.0,<6.0

# ── Runtime stage ───────────────────────────────────────────────────
FROM python:3.11-slim-bookworm

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local/lib/python3.11/site-packages

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
