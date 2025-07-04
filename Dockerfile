FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.6.1

# Set work directory
WORKDIR /app

# Copy Poetry files and README (needed for Poetry package installation)
COPY pyproject.toml poetry.lock README.md ./

# Copy application code (needed for Poetry package installation)
COPY ./app ./app

# Configure Poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only=main \
    && rm -rf $POETRY_CACHE_DIR

# Create non-root user
RUN adduser --disabled-password --gecos '' --uid 1000 apiuser

# Change ownership of app directory
RUN chown -R apiuser:apiuser /app

# Switch to non-root user
USER apiuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]