# VibeSDK Project Overview

## 1) Executive Summary
VibeSDK is an open-source, full-stack AI app generation platform that lets users describe an app in natural language and receive a runnable, deployable web application. This repository is a production-grade implementation of that platform, built primarily for Cloudflare infrastructure.

Current package version: `1.4.0`.

## 2) What the Product Does (Non-Technical)
- Converts user prompts into working apps through an interactive chat workflow.
- Supports iterative collaboration: users can refine requirements and regenerate code in phases.
- Provides live previews so users can test generated apps before deployment.
- Enables publishing generated apps to Cloudflare and exporting code to GitHub.
- Includes a public/private app experience with discovery, favorites, and starring.

## 3) Target Users and Value
- Teams building AI-powered internal/external app builders.
- Product and operations teams that need rapid prototyping without full manual coding.
- SaaS builders who want "build with prompt" capabilities in their platform.

Primary value:
- Faster time-to-prototype.
- Lower barrier for non-engineering users.
- Cloud-native deployment path with integrated security and observability patterns.

## 4) Core Feature Set
- AI code generation modes:
  - `phasic`: deterministic phase-based generation.
  - `agentic`: more autonomous generation behavior.
- Real-time generation events over WebSockets.
- Sandbox preview deployment for generated apps.
- Cloudflare deployment path for generated apps.
- App lifecycle features: create, view, list, favorites, stars, visibility controls, delete.
- Authentication features: email flows + OAuth providers, session management, API key management.
- SDK (`@cf-vibesdk/sdk`) for programmatic app generation and session control.
- GitHub export integration and git clone token support.
- Platform capabilities/status APIs and analytics routes.

## 5) Technical Architecture
### Frontend
- React + TypeScript + Vite.
- React Router based app shell and route modules (`/`, `/chat/:chatId`, `/apps`, `/app/:id`, `/discover`, profile/settings).
- Component-driven UI with hooks/contexts for auth, app data, and chat workflows.

### Backend
- Cloudflare Worker runtime with Hono API framework.
- Durable Objects for stateful agent sessions and related services.
- Real-time communication for generation/progress via WebSocket endpoints.
- API grouping includes auth, apps, codegen, model config/providers, analytics, status, capabilities, screenshots, and GitHub export.

### Data and Platform Services
- D1 (SQLite) for core application data.
- KV for fast key-value/session-like storage.
- R2 for templates/assets.
- Cloudflare Containers for sandbox execution and previews.
- Dispatch namespace routing for user-deployed apps on subdomains.
- AI Gateway for multi-provider model routing and observability.

## 6) Security and Reliability Highlights
- Secure headers and CORS controls in worker middleware.
- CSRF protection (double-submit cookie pattern).
- Route-level auth policies (public/authenticated/owner-only).
- Rate limiting at platform level and per route families.
- Secret handling patterns including dedicated secret storage DO.
- Structured logging and optional Sentry integration.

## 7) Developer Experience and Operations
- Scripts for setup, development, typecheck, lint, tests, DB migration, and deployment.
- Drizzle ORM + migration flow for local and remote D1.
- Deployment model supports local-first development and Cloudflare production rollout.
- Requires Cloudflare account/resources and at least one configured AI provider key.

## 8) Business and Governance Notes
- License: MIT.
- Open-source and intended for customization/extension.
- Repository includes active release cadence and extensive changelog updates around model support, reliability, and SDK maturity.

## 9) High-Level Risks/Considerations
- Production usage depends on correct Cloudflare resource setup and token permissions.
- AI provider/model quality, latency, and cost are external dependencies.
- Sandbox and multi-service orchestration increases operational complexity at scale.
