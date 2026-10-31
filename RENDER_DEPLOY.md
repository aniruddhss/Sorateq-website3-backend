# Deploying Sorateq Backend to Render

This backend is pre-configured for deployment as a **Web Service** on [Render](https://render.com).

---

## Deployment Option 1: Automatic Blueprint (Recommended)

1. Push this repository to GitHub / GitLab.
2. In your [Render Dashboard](https://dashboard.render.com/), click **New +** > **Blueprint**.
3. Select your repository. Render will automatically read `render.yaml` and configure:
   - Root directory: `.` (repository root)
   - Build command: `bash build.sh`
   - Start command: `bash start.sh`
   - Health check: `/health`
   - Python version: `3.11.9`
4. Set the environment variables in the dashboard (see below).
5. Click **Apply**.

---

## Deployment Option 2: Manual Web Service

1. In Render Dashboard, click **New +** > **Web Service**.
2. Connect your Git repository.
3. Configure the following fields:

| Field | Value |
| :--- | :--- |
| **Name** | `sorateq-backend` (or your choice) |
| **Region** | `Ohio (US East)` (recommended to match Supabase `us-east-2`) |
| **Branch** | `main` |
| **Root Directory** | Leave blank (root of repository) |
| **Runtime** | `Python 3` |
| **Build Command** | `bash build.sh` (or `pip install -r requirements.txt`) |
| **Start Command** | `bash start.sh` (or `uvicorn app.main:app --host 0.0.0.0 --port $PORT`) |
| **Instance Type** | `Free` or `Starter` |

4. Under **Advanced** > **Health Check Path**:
   - Set to: `/health` (or `/api/v1/health`)

---

## Environment Variables to Add in Render

| Variable | Required? | Example / Notes |
| :--- | :---: | :--- |
| `DATABASE_URL` | **Yes** | `postgresql://postgres.[ref]:[password]@aws-0-us-east-2.pooler.supabase.com:5432/postgres` (Auto-converts to asyncpg) |
| `SUPABASE_URL` | Optional | `https://[ref].supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | Optional | Your Supabase service role key |
| `SUPABASE_ANON_KEY` | Optional | Your Supabase anon key |
| `GEMINI_API_KEY` | Optional | Google Gemini API key (for Sora AI) |
| `OPENAI_API_KEY` | Optional | OpenAI API key (for text-embedding-3-small embeddings) |
| `ANTHROPIC_API_KEY` | Optional | Claude API key |
| `ENVIRONMENT` | Recommended | `production` |
| `PYTHON_VERSION` | Recommended | `3.11.9` |
| `CORS_ORIGINS` | Optional | `["https://sorateq.com","https://www.sorateq.com"]` (Defaults to wildcard / Vercel / Render domains) |

> **Note on Database Connection**:
> The backend automatically detects connection strings starting with `postgres://` or `postgresql://` and converts them to `postgresql+asyncpg://` for async queries, while deriving `SYNC_DATABASE_URL` for Alembic migrations. SSL is automatically enabled when connecting to remote cloud databases like Supabase or Render PostgreSQL.

---

## Connecting Next.js Frontend to Deployed Backend

Once your Render backend is live (e.g. `https://sorateq-backend.onrender.com`), configure your frontend environment:

In your Next.js `.env.local` or Vercel dashboard:
```env
FASTAPI_BACKEND_URL=https://sorateq-backend.onrender.com
```

