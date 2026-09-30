# ──────────────────────────────────────────────
# Stage 1: Build — install Python deps
# ──────────────────────────────────────────────
FROM python:3.12-slim AS builder

# Prevent Python from buffering stdout/stderr and writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system packages required by psycopg2-binary and Pillow
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev libjpeg62-turbo-dev zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ──────────────────────────────────────────────
# Stage 2: Runtime — lean final image
# ──────────────────────────────────────────────
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=job_portal.settings_prod

# Runtime libraries needed by psycopg2 and Pillow
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 libjpeg62-turbo zlib1g && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project source code
COPY . .

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Collect static files at build time (needs SECRET_KEY set to any dummy value)
RUN SECRET_KEY=build-placeholder DJANGO_SETTINGS_MODULE=job_portal.settings_prod \
    python manage.py collectstatic --noinput

# Render injects the PORT env var at runtime (defaults to 10000)
EXPOSE 10000

CMD ["./entrypoint.sh"]
