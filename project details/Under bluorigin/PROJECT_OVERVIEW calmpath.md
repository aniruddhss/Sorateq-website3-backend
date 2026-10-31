# CalmPath Project Overview

## 1) What CalmPath Is (Non-Technical)
CalmPath is a dementia and memory-care support platform centered on a voice companion experience.
It is designed for three groups:
- Patients: receive calming, simple voice interactions.
- Family members: personalize care with photos, reminders, and patient context.
- Facility staff: monitor patient status and manage operational workflows.

Product positioning in the UI emphasizes:
- Emotional comfort and companionship.
- Memory recall support through photos and personal stories.
- Practical caregiver operations (patient management, reminders, billing).
- A non-diagnostic wellness stance (not positioned as a medical diagnosis tool).

## 2) Core Feature Set
### Patient-facing experience
- Voice-first companion UI with one-tap start/stop.
- Browser speech recognition and speech synthesis with iOS/Safari handling and text fallback.
- Realtime voice session support via OpenAI Realtime API.
- Conversation timeline with recent exchanges.
- Quick comfort activities:
  - Breathing exercise (guided inhale/hold/exhale cycle).
  - Memory photos viewing.
  - Peaceful content flow (scene/music hooks in UI).
- In-app notifications for due reminders (paused while voice chat is active).

### Family member experience
- Family dashboard with tabs for Overview, Photos, Reminders, Personal Info, Billing.
- Memory photo upload (tags, descriptions, story context) and delete.
- Personal profile details for AI personalization (work history, family, hobbies, food, other).
- Reminder creation and management.
- Medication tracking and removal.
- Subscription management plus facility invite-code based access.

### Facility/staff experience
- Facility dashboard with patient/member status monitoring.
- Patient management (invite/create/delete/update status).
- Facility settings:
  - Branding (name, tagline, logo, color).
  - Billing configuration (monthly price, promo code, Stripe linkage).
  - Invite package purchasing and invite code inventory/limits.
- Admin/debug endpoints for users and statistics.

## 3) Technical Architecture
### Frontend
- Framework: Next.js 15 + React 19 + TypeScript.
- Styling/UI: Tailwind CSS + Radix UI components.
- App structure: App Router with pages for auth, dashboard, family dashboard, billing, and patient main app.
- Client auth state: context-based (`useAuth`) with token persisted in localStorage.

### Backend
- Framework: Express + TypeScript.
- Data layer: Drizzle ORM over PostgreSQL (`pg` pool).
- Session support: `express-session` + `connect-pg-simple`.
- File uploads: `multer` to local `uploads` directory.
- AI service: OpenAI Chat Completions + sentiment/mood handling.
- Voice APIs: OpenAI Realtime session bootstrap + voice processing routes.
- Payments: Stripe Checkout, Billing Portal, invoices, coupon validation, webhook processing.

### Data Model (PostgreSQL)
Major entities include:
- `users`, `facilities`, `patients`
- `conversations`, `sessions`, `user_sessions`
- `alerts`, `mood_logs`, `staff_notes`
- `memory_photos`, `therapeutic_photos`
- `medications`, `reminders`, `personal_info`
- Invite commerce flow: `facility_invite_packages`, `facility_invite_purchases`, `facility_invites`

## 4) Integrations and Infrastructure
- Database target is PostgreSQL, with migration guidance for Supabase.
- Deployment flow documented for EC2 and process managers (PM2).
- Cross-origin support configured for production domains and preview environments.
- Frontend and backend both rely heavily on environment variables for API URLs, OpenAI, Stripe, and DB connectivity.

## 5) Business and Operational Model
- Supports subscription-based access and facility-sponsored invite access.
- Facility can purchase invite bundles and distribute access via invite codes.
- Family users can either pay directly or be covered by facility invites.
- Emphasis on caregiver efficiency and emotionally supportive patient interaction.

## 6) Current Maturity Snapshot
Strengths:
- Broad end-to-end scope (voice AI + caregiving ops + billing + invite monetization).
- Clear role-based experiences (patient/family/facility).
- Practical memory-care oriented data model.

Notable risks/technical debt observed:
- Mixed auth patterns (session + token) and custom base64 token format.
- Very verbose debug logging and numerous debug/test endpoints in production code paths.
- Frontend build config currently ignores TypeScript and ESLint build errors.
- Presence of sensitive-looking values in migration documentation should be reviewed and rotated if real.
- Large monolithic backend route file suggests maintainability challenges.

---
This overview reflects the current codebase state in `d:\sid\calmpath` as analyzed on 2026-04-14.
