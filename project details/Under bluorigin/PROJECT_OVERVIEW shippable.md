# Shippable Project Overview

## 1. What this project is
Shippable is an AI-assisted production-readiness scanner for GitHub repositories. It helps developers decide if code is safe to ship by scanning for security risks, scalability issues, code health problems, and missing production basics.

Primary value proposition:
- Fast launch confidence for "vibe-coded" or rapidly built apps
- Clear verdicts (ready, almost-ready, needs-work, not-ready)
- Actionable findings with file-level context and fix guidance

## 2. Target users and non-technical context
Target users:
- Indie hackers and solo developers
- Startup teams shipping quickly
- Builders who want a pre-launch risk check

Business and product context:
- Beta-stage product with active iteration loops
- Includes post-scan feedback capture and Calendly consultation path
- Includes a waitlist flow for early access and enterprise interest
- Go-to-market docs focus on beta recruitment, user interviews, conversion signals, and pricing experiments

## 3. Core user journey
1. User lands on homepage and connects GitHub.
2. User selects one repo (or multiple repos with roles) on dashboard.
3. User chooses scan mode and optional AI model.
4. Scan runs with progress updates (SSE-based for single-repo progress/streaming pages).
5. Report page shows prioritized findings and launch-readiness output.
6. User submits next-action feedback (fix now, ship anyway, ask for help, ignore).

## 4. Feature summary
Single-repo scanning:
- Pattern-based scanning across 11 scanner categories
- Optional AI augmentation (ultra-fast and deeper modes)
- Verdict calculation based on severity and issue counts

Multi-repo system scanning:
- Up to 3 repositories in one scan request
- Repo role assignment (frontend/backend/api/mobile/database/microservice/other)
- Cross-repo compatibility checks (API contract, CORS, auth method, version mismatch, env consistency)

Streaming and progress UX:
- Non-stream scan endpoint returning full results
- SSE progress endpoint for step-by-step scan updates
- SSE stream endpoint for live findings and incremental cost tracking
- Resume-token support in streaming scan flow

Reporting UX:
- Findings grouped by severity and category
- Report built from normalized scanner signals
- Multi-repo results flattened for unified report view in current UI

Operational features:
- Daily scan-rate limiting per user
- Cost estimation guardrails before AI scans
- Error logging and scan metrics persistence
- Admin stats endpoint for user/scan/error visibility

Growth features:
- Waitlist capture backed by Supabase
- Feedback capture endpoint

## 5. Technical architecture
Framework and language:
- Next.js App Router
- TypeScript
- React 19
- Tailwind CSS 4

Key integrations:
- GitHub API via Octokit
- OpenAI API for AI analysis
- Supabase (PostgreSQL) for persistence

Auth model:
- Hybrid auth strategy:
  - Preferred: GitHub App installation flow
  - Fallback: OAuth token flow
- Server resolves auth context from installation cookie or OAuth token cookie

Data layer:
- Active runtime persistence uses Supabase helpers in lib/supabase.ts
- Supabase schema includes users, scans, findings, feedback, error logs, AI usage metrics, multi-repo entities, and compatibility issues
- Waitlist endpoint inserts directly into Supabase waitlist table

Scanner layer:
- Modular scanner files under lib/scanner
- 11 baseline scanner modules + AI deep/smart/ultra-cheap scanners
- Normalization + capping pipeline before report/verdict

## 6. Configuration and environment
Common required environment variables:
- GitHub auth variables (GitHub App and/or OAuth credentials)
- NEXT_PUBLIC_APP_URL
- NEXT_PUBLIC_SUPABASE_URL
- SUPABASE_SERVICE_ROLE_KEY
- OPENAI_API_KEY (for AI-enhanced scans)
- MAX_SCANS_PER_USER, MAX_SCAN_COST, MAX_MULTIREPO_COUNT (optional operational limits)

## 7. Current implementation status notes
- The runtime code is Supabase-based for persistence and rate limiting.
- The repository still contains Airtable migration/setup docs and Airtable helper code, indicating transition history.
- Product docs include both older and newer UX narratives; live code includes multi-repo and streaming paths.

## 8. Project maturity snapshot
Strengths:
- Broad scanner coverage with modular architecture
- Practical safeguards (rate/cost limits, error logging)
- End-to-end flow from scan to feedback to consultation

Current constraints:
- Some documentation is legacy or partially out of sync with current runtime behavior
- Feature set is beta-oriented and still evolving
