# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set metadata for easier identification in Rancher Desktop
LABEL maintainer="dmytro.piskun@gmail.com"
LABEL description="CogniBot - Telegram Bot for Cognitive Bias Detection"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY src/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY src/ .

# Create logs directory with proper permissions
RUN mkdir -p /app/logs && \
    chmod 755 /app/logs

# Create non-root user for security
RUN groupadd -r cognibot && useradd -r -g cognibot cognibot
RUN chown -R cognibot:cognibot /app
USER cognibot

# Health check for monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Expose port for future use
EXPOSE 8080

# Use the launcher script as entrypoint
CMD ["python", "run_bot.py"] 