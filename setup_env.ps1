# Sorateq Backend Setup Script (Windows PowerShell)

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Setting up Sorateq FastAPI & pgvector   " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. Create Virtual Environment
if (!(Test-Path -Path "venv")) {
    Write-Host "[1/4] Creating Python virtual environment (venv)..." -ForegroundColor Yellow
    python -m venv venv
} else {
    Write-Host "[1/4] Virtual environment already exists." -ForegroundColor Green
}

# 2. Activate Virtualenv and Install Requirements
Write-Host "[2/4] Installing dependencies from requirements.txt..." -ForegroundColor Yellow
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\pip.exe install -r requirements.txt

# 3. Environment Config
if (!(Test-Path -Path ".env")) {
    Write-Host "[3/4] Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "Please configure your DATABASE_URL (Supabase/PostgreSQL) and API keys in backend/.env" -ForegroundColor Magenta
} else {
    Write-Host "[3/4] .env file already exists." -ForegroundColor Green
}

Write-Host "[4/4] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To run Alembic database migrations:" -ForegroundColor White
Write-Host "  .\venv\Scripts\alembic.exe upgrade head" -ForegroundColor Cyan
Write-Host ""
Write-Host "To ingest all 44 projects and knowledge base embeddings:" -ForegroundColor White
Write-Host "  .\venv\Scripts\python.exe scripts/ingest_knowledge.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the FastAPI development server:" -ForegroundColor White
Write-Host "  .\venv\Scripts\uvicorn.exe app.main:app --reload --port 8000" -ForegroundColor Cyan
