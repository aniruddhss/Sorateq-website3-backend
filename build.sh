#!/usr/bin/env bash
# Render Build Script
set -e

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

echo "==> Build complete."

