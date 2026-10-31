"""
Loads the Next.js JSON store's knowledge content into Supabase `knowledge_items`:
knowledge docs, capabilities, methodology steps, and FAQs.

Dry run by default. Pass --apply to write. Upserts by ID, so re-running is safe.

Usage (from backend/):
    python scripts/migrate_knowledge_to_supabase.py            # dry run
    python scripts/migrate_knowledge_to_supabase.py --apply    # write
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
    """The JSON store keys some collections by ID and stores others as lists."""
    if isinstance(collection, dict):
        return list(collection.values())
    return list(collection or [])


def build_items(store: dict) -> list[tuple]:
    rows: list[tuple] = []

    for d in as_list(store.get("knowledgeDocs")):
        rows.append((
            d["id"], d.get("category", "company"), d["title"], d["content"],
            d.get("summary"), d.get("visibility", "PUBLIC"),
            json.dumps(d.get("tags", [])), json.dumps(d.get("metadata", {})),
        ))

    for c in as_list(store.get("capabilities")):
        content = "\n".join(filter(None, [
            c.get("shortDescription"), c.get("fullDescription"),
            "Deliverables: " + "; ".join(c.get("deliverables", [])) if c.get("deliverables") else None,
        ]))
        rows.append((
            c["id"], "capabilities", c["title"], content, c.get("shortDescription"),
            c.get("visibility", "PUBLIC"), json.dumps(c.get("tags", [])),
            json.dumps({"slug": c.get("slug")}),
        ))

    for s in store.get("methodology", []):
        step_id = f"method-{s['step']}"
        content = "\n".join(filter(None, [
            s.get("description"),
            "Deliverables: " + "; ".join(s.get("deliverables", [])) if s.get("deliverables") else None,
        ]))
        rows.append((
            step_id, "methodology", s["title"], content, s.get("description"), "PUBLIC", json.dumps([]),
            json.dumps({
                "step": s["step"],
                "subtitle": s.get("subtitle", ""),
                "description": s.get("description", ""),
                "deliverables": s.get("deliverables", []),
                "duration": s.get("duration", ""),
            }),
        ))

    for f in as_list(store.get("faqs")):
        rows.append((
            f["id"], "faqs", f["question"], f["answer"], None,
            f.get("visibility", "PUBLIC"), json.dumps(f.get("tags", [])),
            json.dumps({"faqCategory": f.get("category")}),
        ))

    return rows


UPSERT_SQL = """
insert into knowledge_items (id, category, title, content, summary, visibility, tags, metadata_json)
values ($1,$2,$3,$4,$5,$6,$7::jsonb,$8::jsonb)
on conflict (id) do update set
  category = excluded.category, title = excluded.title, content = excluded.content,
  summary = excluded.summary, visibility = excluded.visibility, tags = excluded.tags,
  metadata_json = excluded.metadata_json, updated_at = now()
"""


async def run(apply: bool) -> None:
    store = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    rows = build_items(store)

    by_cat: dict[str, int] = {}
    for r in rows:
        by_cat[r[1]] = by_cat.get(r[1], 0) + 1
    print(f"Source: {JSON_PATH}")
    print(f"Items to upsert: {len(rows)} {by_cat}")
    print(f"Mode: {'APPLY' if apply else 'DRY RUN (no writes)'}")

    if not apply:
        for r in rows[:3]:
            print(f"  would upsert: [{r[1]}] {r[0]} - {r[2][:60]}")
        return

    conn = await asyncpg.connect(db_url(), statement_cache_size=0, timeout=30)
    try:
        async with conn.transaction():
            for r in rows:
                await conn.execute(UPSERT_SQL, *r)
        total = await conn.fetchval("select count(*) from knowledge_items")
        print(f"Done. knowledge_items now has {total} rows.")
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
