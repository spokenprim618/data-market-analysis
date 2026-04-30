FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (optional but recommended for ML stacks)
RUN apt-get update && apt-get install -y \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (for Docker layer caching)
COPY requirements.txt .
COPY constraints.txt .

# Copy install scripts
COPY scripts/sh_scripts/install_cpu_stack.sh /app/install_cpu_stack.sh

# Make script executable
RUN chmod +x /app/install_cpu_stack.sh

# Run controlled CPU-only install
RUN /app/install_cpu_stack.sh

# Copy application code last
COPY . .

