"""
One-time loader: copies the Next.js JSON store (data/sorateq-db.json) into Supabase.

Dry run by default. Pass --apply to write. Upserts are keyed by natural IDs,
so the script is safe to re-run.

Usage (from backend/):
    python scripts/migrate_json_to_supabase.py            # dry run
    python scripts/migrate_json_to_supabase.py --apply    # write
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import asyncpg

BACKEND_ROOT = Path(__file__).resolve().parents[1]
candidates = [
    BACKEND_ROOT / "data" / "sorateq-db.json",
    BACKEND_ROOT.parent / "frontend" / "data" / "sorateq-db.json",
    BACKEND_ROOT.parent / "data" / "sorateq-db.json",
]
JSON_PATH = next((p for p in candidates if p.exists()), candidates[0])


def db_url() -> str:
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    url = os.environ["DATABASE_URL"]
    return url.replace("postgresql+asyncpg://", "postgresql://")


def load_store() -> dict:
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)


def project_row(p: dict) -> tuple:
    return (
        p["id"], p["slug"], p["name"], p.get("tagline"), p["summary"],
        p.get("fullDescription"), p["industry"], p["projectType"],
        p.get("problem"), p.get("solution"),
        json.dumps(p.get("features", [])), json.dumps(p.get("technologies", [])),
        json.dumps(p.get("services", [])), p.get("stage"), p.get("projectOutcome"),
        p.get("proof"), json.dumps(p.get("metrics", [])), p.get("publicUrl"),
        p.get("caseStudyContent"), bool(p.get("featured")), p.get("visibility", "PUBLIC"),
        json.dumps(p.get("tags", [])), json.dumps(p.get("keywords", [])),
    )


PROJECT_SQL = """
insert into projects (
  id, slug, name, tagline, summary, full_description, industry, project_type,
  problem, solution, features, technologies, services, stage, project_outcome,
  proof, metrics, public_url, case_study, featured, visibility, tags, keywords
) values (
  $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11::jsonb,$12::jsonb,$13::jsonb,$14,$15,$16,
  $17::jsonb,$18,$19,$20,$21,$22::jsonb,$23::jsonb
)
on conflict (slug) do update set
  name = excluded.name, tagline = excluded.tagline, summary = excluded.summary,
  full_description = excluded.full_description, industry = excluded.industry,
  project_type = excluded.project_type, features = excluded.features,
  technologies = excluded.technologies, services = excluded.services,
  metrics = excluded.metrics, public_url = excluded.public_url,
  featured = excluded.featured, visibility = excluded.visibility,
  tags = excluded.tags, keywords = excluded.keywords, updated_at = now()
"""


async def run(apply: bool) -> None:
    store = load_store()
    projects = [p for p in store.get("projects", {}).values() if p.get("visibility") != "PRIVATE"]

    print(f"Source: {JSON_PATH}")
    print(f"Projects to sync: {len(projects)}")
    print(f"Mode: {'APPLY' if apply else 'DRY RUN (no writes)'}")

    if not apply:
        for p in projects[:3]:
            print(f"  would upsert: {p['slug']} ({p['name']})")
        return

    conn = await asyncpg.connect(db_url(), statement_cache_size=0, timeout=30)
    try:
        async with conn.transaction():
            for p in projects:
                await conn.execute(PROJECT_SQL, *project_row(p))
        count = await conn.fetchval("select count(*) from projects")
        print(f"Done. projects table now has {count} rows.")
    finally:
        await conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write to Supabase")
    args = parser.parse_args()
    try:
        asyncio.run(run(args.apply))
    except Exception as exc:  # noqa: BLE001
        print(f"Failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)
