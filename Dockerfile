FROM python:3.11-slim

WORKDIR /app

# -------------------------
# System dependencies
# -------------------------
RUN apt-get update && apt-get install -y \
    bash \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# Copy dependency files
# -------------------------
COPY requirements.txt .
COPY constraints.txt .

# -------------------------
# Copy install script
# -------------------------
COPY scripts/sh_scripts/install_cpu_stack.sh /app/install_cpu_stack.sh

RUN chmod +x /app/install_cpu_stack.sh

# -------------------------
# Install Python stack
# -------------------------
RUN /app/install_cpu_stack.sh

# -------------------------
# Install spaCy model (IMPORTANT)
# -------------------------
RUN python -m spacy download en_core_web_sm
# -------------------------
# Copy app code last
# -------------------------
COPY . .