#!/usr/bin/env bash
set -e

echo "📦 Step 1: Installing CPU-only PyTorch (LOCKED)"

pip install --no-cache-dir \
  torch==2.2.2 \
  --index-url https://download.pytorch.org/whl/cpu

echo "📦 Step 2: Installing core NLP stack (constrained)"

pip install --no-cache-dir \
  -r requirements.txt \
  -c constraints.txt

echo "📦 Step 3: Installing transformer stack manually (NO dependency resolution)"

pip install --no-cache-dir \
  transformers==4.41.2 \
  tokenizers==0.19.1 \
  --no-deps

pip install --no-cache-dir \
  sentence-transformers==2.7.0 \
  --no-deps

echo "🔍 Verifying no CUDA packages..."

if pip list | grep -E "nvidia|cuda|triton" > /dev/null; then
    echo "❌ CUDA PACKAGES DETECTED"
    pip list | grep -E "nvidia|cuda|triton"
    exit 1
fi

echo "✅ CPU ENV READY"