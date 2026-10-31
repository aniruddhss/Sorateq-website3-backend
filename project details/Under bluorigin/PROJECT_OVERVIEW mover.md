# MOVER Project Overview

## 1. Executive Summary
MOVER is an AI-first motion graphics platform that converts user prompts into editable Remotion React animations. The product combines AI code generation, a live preview/code editor, project history, collaborative-style showcase publishing, and admin operations tooling.

At implementation level, the codebase is split into:
- `mover-frontend`: Next.js app for UX, AI generation APIs, Remotion preview, and Lambda render endpoints.
- `mover-backend/backend`: Express + TypeScript API for authentication, persistence, admin, showcase, and stitch project data.

## 2. Product and Non-Technical Profile
- Product category: Creative tooling / AI video editor / motion design assistant.
- Primary user promise: "Describe animation intent in plain language, get production-ready motion code fast."
- Current stage: Beta and early-access positioning is visible in product UI and pricing.
- Audience fit: Creators, marketers, social teams, founders, and designers who need quick motion outputs without building every animation manually.
- Go-to-market signals in-app:
- Landing page optimized for prompt-first conversion.
- Waitlist workflows for upcoming features.
- Showcase browsing and remix loops for discovery and retention.
- Legal/privacy pages present (`/terms`, `/privacy`) with product-facing policy copy.

## 3. Core Feature Set
- Prompt-to-animation generation:
- Prompt validation (motion-graphics intent classifier).
- Skill detection and dynamic skill-injection for generation quality.
- Streaming generation with model metadata and token usage events.

- Conversational iteration:
- Follow-up edit mode supports targeted code edits or full replacement.
- Edit failure recovery for ambiguous replacements.
- Auto-correction hooks for compile/runtime issue recovery.

- Visual-input workflows:
- Image attachments in generation context.
- Logo Animator: SVG upload plus prompt-guided per-element motion planning and code synthesis.

- Audio-assisted generation:
- Audio toolchain integration (`generate_complete_audio` and related tools).
- Audio-code injection and import auto-fixes in generated Remotion code.

- Editor and preview:
- Monaco-based code editing.
- Live Remotion preview with frame controls.
- Duration/FPS extraction from generated code.

- Project memory and history:
- Chat/project persistence.
- Version snapshots per generation/edit.
- Message history persistence per project.

- Stitch Mode (multi-clip pipeline):
- Stitch project CRUD.
- Clip CRUD and drag-reorder.
- Transition management between clips.
- Per-clip versions and per-clip messages.
- Shared variables, project theme, and master prompt for continuity.
- Compiled stitched timeline preview with transition overlap logic.

- Showcase/community:
- Publish project from chat history.
- Public listing, filtering, searching, sorting.
- Like/unlike and view tracking.
- Remix-friendly project viewing flow.

- Admin operations:
- First-admin bootstrap flow.
- Admin dashboard stats and analytics endpoints.
- User management (status/plan/role updates, ban/unban, delete).
- Admin logs for action tracking.
- Waitlist management (list/filter/notify/delete/export in UI).

## 4. Technical Architecture
- Frontend stack:
- Next.js 16 + React 19 + TypeScript.
- Remotion 4 ecosystem (`@remotion/player`, `@remotion/lambda`, transitions/shapes/media).
- AI SDK (`ai`, `@ai-sdk/openai`) with streaming + structured outputs.
- NextAuth (Google + Credentials providers).
- Tailwind-based UI system.

- Backend stack:
- Express 4 + TypeScript.
- SQLite via `better-sqlite3`.
- JWT auth + refresh session tracking.
- Route modules for auth, chats, versions, messages, admin, waitlist, showcase, stitch.

- Render stack:
- Local preview and local render hooks.
- AWS Remotion Lambda endpoints for MP4 export (`/api/lambda/render`, `/api/lambda/stitch-render`, `/api/lambda/progress`).

## 5. Data Model (Persistence Layer)
Main database entities in backend SQLite:
- Identity/session: `users`, `sessions`.
- Creative workspace: `chats`, `versions`, `messages`.
- Growth/community: `waitlist`, `published_projects`, `project_likes`.
- Operations: `admin_logs`, `platform_metrics`.
- Stitch domain: `stitch_projects`, `stitch_clips`, `stitch_transitions`, `stitch_clip_versions`, `stitch_clip_messages`.

This schema supports both single-animation and multi-clip stitched workflows with ownership checks and version history.

## 6. Integrations and External Dependencies
- OpenAI:
- Prompt validation and skill detection.
- Main code generation and follow-up editing.
- Vision-assisted logo analysis path.
- TTS in sound-engine modules.

- Optional audio providers:
- Suno (music) and ElevenLabs (SFX), wired through sound-engine tools.

- Authentication:
- Google OAuth via NextAuth.
- Backend sync endpoint for Google sign-in user provisioning.

- Analytics and product telemetry:
- GTM integration present.
- Microsoft Clarity optional via environment variable.

- Infrastructure:
- AWS credentials required for Remotion Lambda rendering.

## 7. Security and Platform Notes
- Positive controls:
- Role-based admin guards (`requireAuth`, `requireAdmin`).
- Ownership checks on user-scoped resources.
- JWT-based auth and refresh-session table.

- Important risks/limitations to track:
- Backend has a default fallback JWT secret (`sova-dev-secret-change-in-production`) if env is missing.
- Access/refresh tokens are also handled in browser storage flows, so deployment hardening is important.
- SQLite backend is operationally simple but can become a bottleneck under high concurrent load.

## 8. Business and UX Signals
- Monetization intent is explicit in pricing UX:
- Base subscription ($19/month shown in pricing page).
- Usage-style AI generation pricing messaging and credit concept.

- Retention/community loops include:
- Saved project/version history.
- Public showcase and likes.
- Remix entry points.

- Operational readiness signals:
- Dedicated admin panel for user and content operations.
- Waitlist and outreach management built into platform workflows.

## 9. Current Maturity Assessment
Overall status: strong beta-stage implementation with real product depth.

What is production-leaning already:
- Full-stack auth and persistence.
- Multi-mode generation (single clip + stitch).
- Public showcase and admin operations.
- Lambda export pathways.

What appears partially complete or inconsistent:
- Naming/doc drift: code and docs still mix `SOVA` and `MOVER` naming.
- Some docs reference older/legacy setup assumptions (for example, stale backend readme context).
- Onboarding UI path exists but is currently disabled in dashboard flow.
- Several capability docs are ahead of or parallel to implementation details; periodic documentation consolidation is recommended.

## 10. One-Line Project Characterization
MOVER is a full-stack AI motion studio: prompt-to-Remotion generation at the core, with persistent creative workflow, multi-clip stitching, social showcase, and admin-grade operational tooling around it.
