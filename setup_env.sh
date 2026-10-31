#!/usr/bin/env bash
set -e

echo "========================================="
echo " Setting up Sorateq FastAPI & pgvector   "
echo "========================================="

# 1. Create Virtual Environment
if [ ! -d "venv" ]; then
    echo "[1/4] Creating Python virtual environment (venv)..."
    python3 -m venv venv
else
    echo "[1/4] Virtual environment already exists."
fi

# 2. Activate Virtualenv and Install Requirements
echo "[2/4] Installing dependencies from requirements.txt..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. Environment Config
if [ ! -f ".env" ]; then
    echo "[3/4] Creating .env from .env.example..."
    cp .env.example .env
    echo "Please configure your DATABASE_URL (Supabase/PostgreSQL) and API keys in backend/.env"
else
    echo "[3/4] .env file already exists."
fi

echo "[4/4] Setup complete!"
echo ""
echo "To run Alembic database migrations:"
echo "  alembic upgrade head"
echo ""
echo "To ingest all 44 projects and knowledge base embeddings:"
echo "  python scripts/ingest_knowledge.py"
echo ""
echo "To start the FastAPI development server:"
echo "  uvicorn app.main:app --reload --port 8000"
