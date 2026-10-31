# Securefront Project Overview

## Project Summary
Securefront is a compliance management platform for organizations that need to track regulatory readiness across staff, locations, vendors, and audit workflows. It combines an admin dashboard, role-based operations, compliance item tracking, and audit export capabilities in one system.

## Non-Technical Overview
- Primary goal: reduce compliance risk and audit preparation time.
- Intended users: compliance officers, operations/admin teams, managers, and external participants using secure onboarding links.
- Business value:
  - Centralized visibility of compliance status.
  - Faster response to expiring or missing requirements.
  - Standardized workflows for onboarding and document collection.
  - Better accountability via activity history and audit exports.

## Technical Architecture
- Monorepo area: `securefront`
- Frontend app: `Compliance_Tool_FrontendSF`
- Backend app: `Compliance_Tool_BackendSF`

### Frontend
- Framework: Next.js 16, React 19, TypeScript.
- UI: Tailwind CSS + Radix UI style component system.
- State/data: SWR for fetch/revalidation, context-based auth state.
- Auth modes:
  - Supabase Auth mode.
  - Legacy backend JWT mode with token refresh.

### Backend
- Framework: Express.js.
- API docs: Swagger (`/api-docs`).
- Auth:
  - JWT access tokens.
  - Refresh token cookie flow.
- Authorization:
  - RBAC permissions + role-based checks.
  - Company scoping and location access controls.
- Export engine:
  - Audit preview and export in PDF or CSV.

### Data Layer
- Primary runtime target: Supabase/Postgres.
- Legacy compatibility paths: SQLite-based logic still present in parts of the code.
- Core entities:
  - companies
  - users
  - staff
  - locations
  - roles
  - compliance_requirements
  - compliance_items
  - activity_logs
  - sessions

### Deployment and Operations
- Both apps include Railway deployment config.
- Frontend and backend are split services.
- Environment variable driven setup for auth, DB, API URLs, and feature flags.

## Key Product Features
- Authentication: signup, login, logout, refresh, profile retrieval.
- Dashboard: compliance health and organization summary.
- Locations: create, list, update, remove, filter.
- Staff management: create, profile, update, remove, role links.
- Roles and permissions: role CRUD, requirement assignment, staff assignment.
- Compliance registry:
  - Define compliance requirements.
  - Assign requirements to staff and locations.
  - Track requirement metadata and renewal windows.
- User management:
  - Admin user creation and role assignment.
  - Manager hierarchy and location-scoped access.
- Activity tracking: timeline-style action logs.
- Audit center:
  - Live filtered preview.
  - Export to PDF/CSV.
- External onboarding:
  - Magic-link verification.
  - Document upload and completion flow.

## Engineering Maturity Snapshot
### Strengths
- Broad feature surface covering core compliance operations.
- Backend includes route-level automated tests (Jest + Supertest).
- Clear separation between frontend and backend responsibilities.

### Current Gaps / Risks
- Mixed naming conventions and legacy/modern field formats in some paths.
- Some frontend onboarding and utility screens include simulated flow behavior.
- Frontend build currently allows TypeScript build errors (`ignoreBuildErrors: true`).
- Auth and data access support dual modes, which increases complexity.

## Suggested Next Priorities
1. Standardize data contracts (snake_case vs camelCase) across frontend/backend.
2. Remove or harden prototype-like onboarding behaviors for production.
3. Disable TypeScript build-error bypass in frontend once type issues are resolved.
4. Consolidate fully on Supabase path if SQLite fallback is no longer required.
5. Add frontend tests for critical auth and onboarding user journeys.
