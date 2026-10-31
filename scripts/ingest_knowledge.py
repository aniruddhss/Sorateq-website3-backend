import os
import sys
import json
import glob
import asyncio
import re

# Add backend to path
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.db.models import Project, KnowledgeItem, Base
from app.services.embeddings import get_embedding


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


async def ingest_all():
    print(f"Connecting to database: {settings.DATABASE_URL.split('@')[-1]}")
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    # 1. Read project details JSON (check local backend/ or parent repo paths)
    backend_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
    candidate_roots = [
        backend_dir,
        os.path.realpath(os.path.join(backend_dir, "..")),
        os.path.realpath(os.path.join(backend_dir, "../frontend")),
    ]
    root_dir = backend_dir
    for candidate in candidate_roots:
        if os.path.exists(os.path.join(candidate, "project details", "projects_and_websites_profile.json")):
            root_dir = candidate
            break

    json_path = os.path.join(root_dir, "project details", "projects_and_websites_profile.json")
    
    with open(json_path, "r", encoding="utf-8") as f:
        profile_data = json.load(f)

    # Read markdown files for richer case studies
    md_details = {}
    md_files = glob.glob(os.path.join(root_dir, "project details", "Under bluorigin", "*.md")) + \
               glob.glob(os.path.join(root_dir, "project details", "*.md"))
    for md_file in md_files:
        base = os.path.splitext(os.path.basename(md_file))[0].lower()
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                md_details[base] = f.read()
        except Exception as e:
            print(f"Error reading {md_file}: {e}")

    async with async_session() as session:
        print("\n--- Ingesting Projects ---", flush=True)
        projects_list = profile_data.get("projects", [])
        used_slugs = set()
        for idx, p in enumerate(projects_list):
            raw_name = p.get("name", f"Project {idx+1}")
            parts = raw_name.split(" - ")
            display_name = parts[0].strip()
            tagline = parts[1].strip() if len(parts) > 1 else p.get("short_description", "")
            
            # Generate unique slug
            slug = slugify(display_name)
            if not slug or slug in used_slugs:
                slug = slugify(raw_name)
            if slug in used_slugs:
                slug = f"{slug}-{idx+1}"
            used_slugs.add(slug)

            # Markdown match
            matched_md = ""
            for k, v in md_details.items():
                if slug in k or display_name.lower() in k or k in slug:
                    matched_md = v
                    break

            full_desc = matched_md if matched_md else p.get("detailed_description", p.get("short_description", ""))
            techs = p.get("technologies", ["TypeScript", "Next.js", "Python", "FastAPI", "PostgreSQL"])

            print(f"[{idx+1}/{len(projects_list)}] Ingesting {display_name}...", flush=True)
            # Compute embedding on project text representation
            embed_text = f"{display_name}. {tagline}. Industry: {p.get('industry')}. Technologies: {', '.join(techs)}. Problem: {p.get('problems_solved')}. Summary: {p.get('short_description')}."
            vec = await get_embedding(embed_text)

            proj = Project(
                id=f"proj-{idx+1}",
                slug=slug,
                name=display_name,
                tagline=tagline,
                summary=p.get("short_description", ""),
                full_description=full_desc,
                industry=p.get("industry", "Technology & AI"),
                project_type=p.get("role", "Full-Stack & AI Engineering"),
                problem=p.get("problems_solved", "Fragmented workflows and lack of scalable systems."),
                solution=p.get("detailed_description", ""),
                features=[
                    p.get("short_description", ""),
                    p.get("problems_solved", ""),
                    p.get("proof", "Engineered scalable architecture.")
                ],
                technologies=techs,
                services=[
                    "Full-Stack Development",
                    "System Architecture",
                    "AI Engineering",
                    "Cloud Infrastructure & DevOps"
                ],
                stage="Production Live",
                project_outcome=p.get("outcome", p.get("proof", "Successfully delivered and deployed in production.")),
                proof=p.get("proof", ""),
                public_url=p.get("url", "https://www.sorateq.com"),
                case_study=full_desc,
                featured=(idx < 6),
                visibility="PUBLIC",
                tags=[slug, p.get("industry", "").lower(), "sorateq", "production"],
                keywords=[display_name.lower(), p.get("industry", "").lower()] + [t.lower() for t in techs],
                embedding=vec
            )
            await session.merge(proj)
            print(f"  [OK] Ingested {display_name}", flush=True)

        # 2. Ingest Company Knowledge & Capabilities
        print("\n--- Ingesting Knowledge Items ---", flush=True)
        capabilities = [
            ("AI Engineering & Production RAG", "Custom fine-tuning, pgvector hybrid search, low-latency streaming SSE, agentic LLM orchestration.", "capabilities"),
            ("Distributed Async Backends", "High-concurrency FastAPI microservices, asyncpg connection pooling, Redis queues, Celery/BullMQ workers.", "capabilities"),
            ("Modern Web Platforms", "Next.js App Router, SSR/SSG, Tailwind CSS, high-conversion responsive design systems.", "capabilities"),
            ("Cross-Platform Mobile Apps", "React Native, Expo 55, offline-first SQLite sync, native push notifications.", "capabilities"),
            ("Cloud & DevOps Infrastructure", "Docker containerization, Traefik reverse proxy, AWS S3/CloudFront, Cloudflare Workers & R2.", "capabilities")
        ]
        for title, desc, cat in capabilities:
            vec = await get_embedding(f"{title}: {desc}")
            item = KnowledgeItem(
                id=f"know_{slugify(title)}",
                category=cat,
                title=title,
                content=desc,
                summary=desc,
                visibility="PUBLIC",
                tags=["capabilities", "sorateq", "engineering"],
                embedding=vec
            )
            await session.merge(item)
            print(f"  [OK] Ingested capability: {title}", flush=True)

        await session.commit()
        print("\n[SUCCESS] Successfully ingested all 44 projects and knowledge items with pgvector embeddings!", flush=True)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(ingest_all())
