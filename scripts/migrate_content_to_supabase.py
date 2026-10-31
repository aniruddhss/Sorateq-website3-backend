"""
Loads the JSON store's content into the new app tables:
faqs, capabilities, prompt_versions (the active prompt).

Dry run by default. Pass --apply to write. Upserts by ID, so re-running is safe.

Usage (from backend/):
    python scripts/migrate_content_to_supabase.py            # dry run
    python scripts/migrate_content_to_supabase.py --apply    # write
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
    load_dotenv(BACKEND / ".env")
    return os.environ["DATABASE_URL"].replace("postgresql+asyncpg://", "postgresql://")


def as_list(collection) -> list[dict]:
    if isinstance(collection, dict):
        return list(collection.values())
    return list(collection or [])


FAQ_SQL = """
insert into faqs (id, question, answer, category, visibility, tags)
values ($1,$2,$3,$4,$5,$6::jsonb)
on conflict (id) do update set question = excluded.question, answer = excluded.answer,
  category = excluded.category, visibility = excluded.visibility, tags = excluded.tags, updated_at = now()
"""

CAPABILITY_SQL = """
insert into capabilities (id, slug, title, short_description, full_description, deliverables, visibility, tags)
values ($1,$2,$3,$4,$5,$6::jsonb,$7,$8::jsonb)
on conflict (id) do update set slug = excluded.slug, title = excluded.title,
  short_description = excluded.short_description, full_description = excluded.full_description,
  deliverables = excluded.deliverables, visibility = excluded.visibility, tags = excluded.tags, updated_at = now()
"""

PROMPT_SQL = """
insert into prompt_versions (id, version, name, system_prompt, is_active)
values ($1,$2,$3,$4,$5)
on conflict (id) do update set version = excluded.version, name = excluded.name,
  system_prompt = excluded.system_prompt, is_active = excluded.is_active
"""


async def run(apply: bool) -> None:
    store = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    faqs = as_list(store.get("faqs"))
    capabilities = as_list(store.get("capabilities"))
    prompts = as_list(store.get("promptVersions"))
    active_id = next((p["id"] for p in prompts if p.get("isActive")), prompts[0]["id"] if prompts else None)

    print(f"Source: {JSON_PATH}")
    print(f"FAQs: {len(faqs)}  capabilities: {len(capabilities)}  prompt versions: {len(prompts)} (active: {active_id})")
    print(f"Mode: {'APPLY' if apply else 'DRY RUN (no writes)'}")
    if not apply:
        return

    conn = await asyncpg.connect(db_url(), statement_cache_size=0, timeout=30)
    try:
        async with conn.transaction():
            for f in faqs:
                await conn.execute(
                    FAQ_SQL, f["id"], f["question"], f["answer"], f.get("category"),
                    f.get("visibility", "PUBLIC"), json.dumps(f.get("tags", [])),
                )
            for c in capabilities:
                await conn.execute(
                    CAPABILITY_SQL, c["id"], c["slug"], c["title"], c.get("shortDescription"),
                    c.get("fullDescription"), json.dumps(c.get("deliverables", [])),
                    c.get("visibility", "PUBLIC"), json.dumps(c.get("tags", [])),
                )
            for p in prompts:
                await conn.execute(
                    PROMPT_SQL, p["id"], p["version"], p["name"], p["systemPrompt"], p["id"] == active_id,
                )
        counts = {
            t: await conn.fetchval(f"select count(*) from {t}")
            for t in ["faqs", "capabilities", "prompt_versions"]
        }
        print(f"Done. {counts}")
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
