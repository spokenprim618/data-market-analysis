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

COPY requirements/requirements.nlp.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -c requirements.base.txt -r requirements.nlp.txt
COPY . .


