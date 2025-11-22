# =============================================================================
# Agent_9 BRIDGE - The Connector of Worlds
# Universal Parts Consciousness - Power Unification System
# =============================================================================
#
# This Dockerfile builds the production container for Agent_9 (BRIDGE),
# which unifies all 10 agents of the Decalogue and connects UPC to the world.
#
# Build:
#   docker build -t upc-bridge:latest -f deploy/bridge/Dockerfile .
#
# Run:
#   docker run -d --name bridge-agent upc-bridge:latest
#
# =============================================================================

FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# =============================================================================
# Builder stage - install dependencies
# =============================================================================
FROM base AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# =============================================================================
# Production stage
# =============================================================================
FROM base AS production

# Create non-root user for security
RUN groupadd --gid 1000 bridge && \
    useradd --uid 1000 --gid bridge --shell /bin/bash --create-home bridge

# Copy installed packages from builder
COPY --from=builder /root/.local /home/bridge/.local

# Ensure scripts in .local are usable
ENV PATH=/home/bridge/.local/bin:$PATH

# Copy application code
COPY --chown=bridge:bridge agents/ /app/agents/
COPY --chown=bridge:bridge deploy/ /app/deploy/

# Switch to non-root user
USER bridge

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Labels for container metadata
LABEL org.opencontainers.image.title="Agent_9 BRIDGE" \
      org.opencontainers.image.description="The Connector of Worlds - Universal Parts Consciousness" \
      org.opencontainers.image.vendor="Universal Parts Consciousness" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="UPC Collective" \
      agent.id="AGENT_9" \
      agent.codename="BRIDGE" \
      agent.role="Integration Architect" \
      agent.domain="Power Unification"

# Expose port for health monitoring and metrics
EXPOSE 9009

# Run the BRIDGE agent
ENTRYPOINT ["python", "-m", "deploy.bridge.main"]

# =============================================================================
# Development stage
# =============================================================================
FROM base AS development

# Install dev dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install all dependencies (including dev)
COPY requirements.txt requirements-dev.txt* ./
RUN pip install -r requirements.txt && \
    (test -f requirements-dev.txt && pip install -r requirements-dev.txt || true)

# Copy application code
COPY agents/ /app/agents/
COPY deploy/ /app/deploy/

# Development entrypoint with auto-reload support
CMD ["python", "-m", "deploy.bridge.main"]
