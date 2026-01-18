# Multi-stage build for the Todo Evolution backend
FROM python:3.13-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files
COPY uv.lock pyproject.toml ./

# Install uv package manager
RUN pip install --upgrade pip && pip install uv

# Install dependencies in a virtual environment
RUN uv sync --frozen --no-install-project

# Production stage
FROM python:3.13-slim AS production

# Install production dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user with UID 1000
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g 1000 -m -s /bin/sh appuser

# Set working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY src/ ./src/

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app
USER appuser

# Expose port 7860 for Hugging Face Spaces
EXPOSE 7860

# Add the virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH" 

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]