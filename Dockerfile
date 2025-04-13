# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies and poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to create wheels
RUN poetry config virtualenvs.create false \
    && poetry export -f requirements.txt --output requirements.txt \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels

# Install dependencies
RUN pip install --no-cache /wheels/* \
    && pip install poetry

# Copy application
COPY pyproject.toml poetry.lock ./
COPY ./auth /app/auth
COPY ./main.py /app/main.py

# Install project in production mode
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Switch to non-root user
USER appuser

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]