# syntax=docker/dockerfile:1.6
FROM python:3.11-slim AS base

WORKDIR /app

# Shared OS dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Shared Python dependencies
COPY requirements/requirements.base.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.base.txt


FROM base AS scraper
WORKDIR /app
COPY requirements/requirements.scraper.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -c requirements.base.txt -r requirements.scraper.txt
COPY . .


FROM base AS analysis
WORKDIR /app
COPY requirements/requirements.analysis.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -c requirements.base.txt -r requirements.analysis.txt
COPY . .


FROM base AS dashboard
WORKDIR /app
COPY requirements/requirements.dashboard.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -c requirements.base.txt -r requirements.dashboard.txt
COPY . .


FROM base AS nlp
WORKDIR /app

# Build toolchain only for NLP image (some deps may compile extensions)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Torch CPU build
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -c requirements.base.txt torch==2.2.2 --index-url https://download.pytorch.org/whl/cpu

# NLP stack
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -c requirements.base.txt \
    spacy==3.5.4 \
    skillNer==1.0.3 \
    transformers==4.41.2 \
    tokenizers==0.19.1 \
    sentence-transformers==2.7.0

# spaCy model
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -c requirements.base.txt \
    https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.5.0/en_core_web_sm-3.5.0-py3-none-any.whl
COPY . .
