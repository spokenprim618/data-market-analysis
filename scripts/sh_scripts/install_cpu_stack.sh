#!/usr/bin/env bash

set -e

echo "📦 Installing CPU-only PyTorch..."

pip install --no-cache-dir torch \
  --index-url https://download.pytorch.org/whl/cpu

echo "📦 Installing requirements with constraints..."

pip install --no-cache-dir -r requirements.txt \
  -c constraints.txt

echo "🔍 Verifying no CUDA packages..."

if pip list | grep -E "nvidia|cuda|triton" > /dev/null; then
    echo "❌ CUDA PACKAGES DETECTED"
    pip list | grep -E "nvidia|cuda|triton"
    exit 1
fi

echo "✅ CPU ENV READY"