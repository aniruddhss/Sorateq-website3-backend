# VVD (Virtual Vocational Development) - Project Overview

**Updated**: June 6, 2026 | **Status**: Active Development

---

## Overview

**What**: Digital learning platform for vocational training with AI-powered career planning, courses, events, gamified rewards, and multi-platform access.

**Users**: Students, institutes, faculty, coordinators, partners

**Core Modules**: Courses & enrollment, Hustle (AI careers), Events, Kudos (rewards), Multi-role RBAC, Razorpay payments, S3 uploads, Gemini AI

---

## Tech Stac

| Layer | Tech |
|-------|------|
| **Backend** | Python 3.11, FastAPI, SQLAlchemy 2.0 async, asyncpg, PostgreSQL |
| **Frontend** | Next.js 14+, TypeScript, Tailwind, shadcn/ui, React Query |
| **Mobile** | Expo 55, React Native, Expo Router |
| **Infra** | Docker, Traefik, Let's Encrypt, AWS S3, Razorpay, Gemini |

---

## Architecture

```
Clients (Web/Mobile/Admin) → Traefik → FastAPI Backend ↔ PostgreSQL, S3, Razorpay, Gemini
```

**Backend** (`vvd-backend/`):
- **Core**: `config.py` (settings), `database.py` (async Postgres), `security.py` (JWT, Argon2), `s3_service.py`, `razorpay_client.py`, `email_service.py`, `gemini_service.py`, `reward_engine.py`
- **Models** (72+ entities): Users, Courses, Events, Hustle, Payments, Kudos, Chat, Feedback, etc.
- **Modules** (16+): `auth/`, `events/`, `hustle/`, `payments/`, `kudos/`, `student/`, `faculty/`, `institute/`, `coordinator/`, `public/`, `webhooks/`, etc.

**Frontend** (`vvd-frontend/`):
- Next.js App Router, API proxies (`/app/api/*`), role-based routes
- Components: tabs, Hustle module, admin dashboard, events
- Auth context + React Query

**Mobile** (`vvd-mobile/`):
- Expo Router with role-based tabs
- Camera/QR, image upload, notifications, Razorpay SDK

---

## Database (72+ Models)

**ORM**: SQLAlchemy 2.0 async | **Driver**: asyncpg | **Migrations**: Alembic

**User Roles**: Student, Faculty, Admin, VVDCoordinator, VVDPartner, ProjectApprover, ChannelManager

**Entities**:
- **Users**: User (base), Admin, Student, Faculty, Coordinator, Partner, Approver, ChannelManager
- **Learning**: Institute, Course, CourseSubject, Subject, StudentSubjectEnrollment, CourseEnrollment, SubjectSession
- **Events**: Event, EventTicket, EventTicketTier, EventCoupon, EventCheckIn, EventAdmin, EventReferralConfig
- **Hustle**: HustleRoadmap, HustleTask, HustleStudentTaskProgress, HustleAIProject, HustleStudentAIProjectSubmission, HustleResume, HustlePayment, HustleRanking
- **Payments**: Payment (polymorphic), MonthlyFeeRecord, Settlement, FeeTransaction
- **Rewards**: KudosWallet, KudosTransaction, KudosRewardRule, KudosRedemption, VVDPartner
- **Misc**: Chat, SupportTicket, Feedback, OTP, DeviceToken, CareerRole, Referral, CollegeCatalog

**Key Relationships**:
```
User → (Student|Faculty|Admin|Partner|Coordinator|Approver|ChannelManager)
Institute → Course → CourseSubject → Subject
Subject → StudentSubjectEnrollment → Student
Event → (EventTicket, EventCoupon, EventCheckIn, EventAdmin)
HustleRoadmap → HustleTask → HustleStudentTaskProgress
Payment (polymorphic) → CourseEnrollment|EventTicket|HustlePayment|MonthlyFeeRecord
KudosWallet ← User → KudosTransaction
```

---

## API Routes

**Auth**: `POST /auth/{register, login, google, refresh, logout, send-otp, verify-otp}`

**Student**: `GET /student/{me, institutes}`, `POST /courses/{id}/buy`, `GET /fees`, `PATCH /me`

**Events**: `GET/POST /events/admin`, `GET /events`, `POST /events/{id}/{buy, verify}`, `GET /apply-coupon`

**Hustle**: `GET /roadmaps`, `PATCH /tasks/{id}/complete`, `GET/POST /projects`, `GET/PATCH /resume`, `POST /subscribe`

**Kudos**: `GET /wallet`, `GET /transactions`, `POST /redeem`, `GET /rules`

**Public**: `GET /discover`, `GET /institutes`, `GET /kudos/info`

**Webhooks**: `POST /webhooks/razorpay/{payment, refund}`

**Frontend Proxies**: `/api/{auth, student, events, hustle, quizzes, onboard}/*` → Backend

---

## Integrations

| Service | Use |
|---------|-----|
| **Razorpay** | Order creation, payment verification (HMAC-SHA256), RazorpayX payouts |
| **Google OAuth** | Multi-client ID, ID token verification |
| **AWS S3** | Presigned URLs (24h), role-based paths, direct browser uploads |
| **Gemini AI** | Roadmap/project/task generation, resume summaries |
| **SMTP/Email** | OTP, confirmations, PDF attachments |
| **Expo Notifications** | Device tokens, push alerts |

---

## Security

- **Passwords**: Argon2id (time=3, memory=64MB, parallelism=4)
- **JWT**: HS256, access (60 min), refresh (30 days), Bearer token
- **Payments**: Webhook signature verification, SELECT FOR UPDATE locking, idempotency via reference tracking
- **CORS**: Whitelist origins, security headers
- **RBAC**: `require_student()`, `require_faculty()` guards
- **Privacy**: Soft deletion, GDPR compliance, 30-day recovery

---

## Deployment

**Containers**: Docker multi-stage (Python 3.11-slim backend, Node 22 frontend)

**Orchestration**: Docker Compose + Traefik reverse proxy

**SSL**: Let's Encrypt auto-renewal

**Database**: PostgreSQL 12+ (cloud-hosted), asyncpg, PgBouncer pooling

**CI/CD**: GitHub Actions (build → push → SSH deploy → healthcheck)

---

## Development

**Backend**:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade heads
python -m uvicorn main:app --reload
```

**Frontend**:
```bash
npm install && npm run dev              # http://localhost:3000
npx tsc --noEmit                        # Type check
npm run lint --fix && npm run build     # Lint & build
```

**Mobile**:
```bash
npm install && npm start                # Expo server
npm run android                         # Android emulator
npm run typecheck                       # Type check
```

**Database**:
```bash
alembic revision --autogenerate -m "description"
alembic upgrade heads
pytest
```

---

## Environment

```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID_WEB=xxxxx
RAZORPAY_KEY_ID=key_xxxxx
RAZORPAY_KEY_SECRET=secret_xxxxx
AWS_ACCESS_KEY_ID=xxxxx
AWS_SECRET_ACCESS_KEY=xxxxx
AWS_S3_BUCKET_NAME=vvd-uploads
GEMINI_API_KEY=xxxxx
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.gmail.com
```

---

## Key Patterns

- **Service Layer**: Business logic in `modules/*/service.py`
- **Dependency Injection**: FastAPI `Depends()` for DB sessions, auth
- **Polymorphic Payment**: Single `Payment` model → multiple entities
- **Soft Delete**: GDPR-compliant deletion with recovery
- **Async-First**: SQLAlchemy 2.0 + asyncpg non-blocking I/O
- **API Gateway**: Next.js proxies for CORS & retry logic

---

## Features

**Hustle**: AI career roadmaps, milestones, auto-generated projects, resume building, subscriptions, leaderboards

**Kudos**: Gamified rewards (earn via quizzes/referrals/purchases), redeem at partners, wallet ledger

**Events**: Tiered pricing, coupons, QR check-in, PDF tickets, referrals

**Multi-Role**: 8 distinct roles with separate permissions

**Payment Hardening**: Idempotent flows, webhook verification, row locking, reference tracking

---

## Status

**✅ Completed**: Auth, RBAC, courses, events, Hustle, Kudos, S3, payments, notifications, 72+ models

**🔄 In Progress**: Guest sessions, public APIs, mobile hardening, quizzes, faculty live sessions

**⚠️ Issues**: Multiple Alembic heads (consolidate), frontend TypeScript linting (run `npm run lint --fix`)

**📋 Planned**: Partner APIs, analytics, bulk ops, ML recommendations

---

## Quick Reference

**Key Files**: `core/config.py`, `core/database.py`, `models/`, `modules/`, `app/` (Next.js), `lib/api/` (clients)

**Common Commands**: 
```bash
docker-compose up              # Local
npm run build                  # Prod build
alembic upgrade heads          # Migrations
pytest                         # Tests
npm run lint --fix && tsc      # Code quality
```

**Details**: See module READMEs and code comments for implementation specifics.

---

**Version**: 2.2 (Ultra-Condensed) | **Maintainers**: VVD Development Team

VVD is a digital learning platform enabling students to build careers through structured vocational training, AI-powered career planning, interactive learning, and reward systems.

**Core Features**:
- Enroll in courses from partner institutes with flexible pacing
- AI-generated personalized career roadmaps with milestone tracking
- Real-world capstone projects for portfolio building
- Live events, webinars, and networking opportunities
- Rewards (Kudos points) for achievements, redeemable at partner brands
- Multiple subscription options (monthly/yearly)
- Web, mobile, and desktop access

**Serves**: Students, institutes, faculty, and corporate partners

### Purpose

VVD is a comprehensive educational platform serving multiple user segments with integrated vocational training, course enrollment, event management, and AI-assisted career development.

### Core Features

- **Courses & Learning**: Enrollment, progress tracking, study materials
- **Hustle Career Module**: AI roadmaps, milestones, capstone projects
- **Events & Ticketing**: Event management, Razorpay integration, QR check-in
- **Kudos Rewards**: Points system with partner redemption
- **Multi-Role System**: Student, Faculty, Admin, Coordinator, Partner, Channel Manager
- **Payments**: Razorpay integration for all transactions
- **File Uploads**: AWS S3 with presigned URLs
- **AI Services**: Google Gemini for content generation

### User Segments

- **Student**: Learn, earn Kudos, attend events
- **Faculty**: Create/teach subjects, grade projects
- **Institute Admin**: Manage institute and faculty
- **VVD Coordinator**: Regional oversight and verification
- **VVD Partner**: Redemption catalog
- **Project Approver**: Evaluate student projects
- **Channel Manager**: Manage events and tickets
- **Super Admin**: Platform oversight

---

## 2. Architecture

### System Architecture

Clients (Web, Mobile, Admin) → Traefik Reverse Proxy → FastAPI Backend ↔ PostgreSQL, AWS S3, Razorpay, Gemini AI

### Architectural Pattern

- **Monolithic Backend**: Single FastAPI application with modular feature organization
- **Stateless APIs**: All state stored in PostgreSQL, compatible with horizontal scaling
- **Async-First**: Built on SQLAlchemy 2.0 async ORM and asyncpg for non-blocking I/O
- **API Gateway**: Frontend/Mobile proxy through Next.js API routes for CORS elimination and retry logic
- **Role-Based Access Control**: Dependency injection guards (e.g., `require_student()`) on protected endpoints
- **Polymorphic References**: Payment model references multiple entities (course, hustle, event) via `payment_for` enum + UUID

---

## 3. Technology Stack

### Core Technologies

| Layer | Technology | Version |
|-------|-----------|---------|
| **Backend Language** | Python | 3.11 |
| **Web Framework** | FastAPI | Latest |
| **ORM** | SQLAlchemy | 2.0+ |
| **Database Driver** | asyncpg | Async |
| **Database** | PostgreSQL | 12+ |
| **Migrations** | Alembic | Latest |
| **Frontend Framework** | Next.js | 14+ |
| **Frontend Language** | TypeScript | 5.0+ |
| **Mobile Framework** | Expo + React Native | 55 / 0.83+ |
| **Build Tool (Web)** | Turbopack | Enabled |
| **Styling** | Tailwind CSS | Latest |
| **UI Components** | shadcn/ui + Radix | Latest |
| **HTTP Client** | Axios / Fetch API | Latest |
| **Forms** | React Hook Form | Latest |
| **Authentication** | JWT (HS256) + Google OAuth | Custom impl |
| **Payment Gateway** | Razorpay | REST API |
| **File Storage** | AWS S3 | REST API |
| **AI Service** | Google Gemini | API |
| **Reverse Proxy** | Traefik | Latest |
| **Container Platform** | Docker + Docker Compose | Latest |

### Backend Dependencies

**Key Libraries**:
- `fastapi` - Web framework
- `sqlalchemy` - ORM
- `alembic` - Migrations
- `asyncpg` - Async Postgres driver
- `pydantic` - Data validation
- `python-jose` - JWT handling
- `argon2-cffi` - Password hashing
- `boto3` - AWS S3
- `razorpay` - Razorpay SDK
- `google-generativeai` - Gemini API
- `aiohttp` - Async HTTP
- `redis` (optional) - Caching/rate limiting

### Frontend Dependencies

**Key Libraries**:
- `next` - Framework
- `react` - UI library
- `typescript` - Type safety
- `@tanstack/react-query` - Data fetching
- `react-hook-form` - Form handling
- `@hookform/resolvers` - Form validation
- `axios` - HTTP client
- `tailwindcss` - Styling
- `shadcn/ui` - Component library
- `razorpay` - Payment SDK
- `ms-clarity` - Analytics
- `leaflet` - Maps

### Mobile Dependencies

- `expo` - Development platform
- `react-native` - Mobile framework
- `expo-router` - Navigation
- `@react-navigation` - Navigation stack
- `@tanstack/react-query` - Data fetching
- `react-native-razorpay` - Payment SDK
- `expo-camera` - QR scanning
- `expo-image-picker` - Media selection
- `expo-notifications` - Push notifications

---

## 4. Backend (vvd-backend)

### Directory Structure

```
vvd-backend/
├── main.py                      # FastAPI entry point
├── requirements.txt             # Dependencies
├── alembic/                     # Database migrations
├── core/                        # Configuration & services (config, database, security, S3, Razorpay, Email, Gemini, etc.)
├── models/                      # 72+ database models (user, courses, events, hustle, payments, kudos, etc.)
├── modules/                     # 16+ feature modules (auth, events, courses, hustle, payments, etc.)
├── scripts/                     # Utility scripts
└── tests/                       # Unit and integration tests
```

### Core Configuration (core/config.py)

Pydantic Settings providing:

```python
# Database
DATABASE_URL: str                    # PostgreSQL connection string
DB_ECHO: bool = False               # SQLAlchemy query logging
DB_POOL_SIZE: int = 20              # Connection pool size
DB_POOL_RECYCLE: int = 3600         # Connection recycle time

# JWT & Authentication
SECRET_KEY: str                      # HS256 signing key
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
REFRESH_TOKEN_EXPIRE_DAYS: int = 30
OTP_EXPIRY_MINUTES: int = 5
OTP_LENGTH: int = 6

# Google OAuth
GOOGLE_CLIENT_ID_MOBILE: str         # Expo/mobile client
GOOGLE_CLIENT_ID_WEB: str            # Web client
GOOGLE_CLIENT_ID_DESKTOP: str        # Desktop client
GOOGLE_CLOCK_SKEW: int = 30          # Token validation tolerance

# Razorpay
RAZORPAY_KEY_ID: str
RAZORPAY_KEY_SECRET: str
RAZORPAY_WEBHOOK_SECRET: str
RAZORPAY_ACCOUNT_NUMBER: str         # For RazorpayX payouts

# AWS S3
AWS_ACCESS_KEY_ID: str
AWS_SECRET_ACCESS_KEY: str
AWS_S3_BUCKET_NAME: str
AWS_S3_REGION: str = "ap-south-1"
S3_PRESIGNED_URL_EXPIRY: int = 86400  # 24 hours

# Email
EMAIL_PROVIDER: str                  # "smtp" | "console" | "disabled"
SMTP_HOST: str
SMTP_PORT: int
SMTP_USERNAME: str
SMTP_PASSWORD: str
EMAIL_FROM: str

# Google Gemini AI
GEMINI_API_KEY: str
GEMINI_MODEL: str = "gemini-2-flash-preview"

# Hustle Pricing
HUSTLE_MONTHLY_PRICE: int = 59900    # ₹599 in paise
HUSTLE_YEARLY_PRICE: int = 599000    # ₹5,990 in paise

# Kudos
MAX_KUDOS_PER_TRANSACTION: int = 500

# Redis (optional)
REDIS_URL: str = None                # For caching/rate limiting

# CORS
CORS_ALLOWED_ORIGINS: List[str]      # Whitelist of frontend origins

# Environment
ENV: str = "production"
```

### Core Services

#### Security (core/security.py)
- **JWT Creation**: `create_access_token(data)` → signed token
- **JWT Verification**: `verify_token(token)` → decoded claims
- **Password Hashing**: Argon2id (time=3, memory=64MB, parallelism=4)
- **Token Types**: Separates "access" and "refresh" via claim

#### S3 Service (core/s3_service.py)
- **Presigned URLs**: 24-hour upload/download links
- **Role-Based Paths**: student-docs/, faculty-docs/, partner-docs/
- **Categories**: Profile photos, ID proofs, event images, documents
- **CORS Support**: Direct browser uploads to S3

#### Razorpay Client (core/razorpay_client.py)
- **Order Creation**: `create_razorpay_order(amount_paise, receipt, notes)`
- **Payment Verification**: Signature validation with HMAC-SHA256
- **Webhook Processing**: Payment capture, refunds, reversals
- **RazorpayX Payouts**: Contact creation, disbursement initiation

#### Email Service (core/email_service.py)
- **Providers**: SMTP (production), Console (dev), Disabled (testing)
- **HTML + Text**: Dual-part emails
- **PDF Attachments**: Event tickets, certificates
- **Use Cases**: OTP delivery, ticket confirmation, support notifications

#### Gemini AI Service (core/gemini_service.py)
- **Roadmap Generation**: Career path creation from goals
- **Task Enrichment**: Learning objectives and resources
- **Project Generation**: Capstone projects at milestones
- **Resume Summarization**: Profile strength assessment
- **Model**: gemini-2-flash-preview (v1alpha)

#### Reward Engine (core/reward_engine.py)
- **Wallet Credit**: `credit_kudos(user_id, amount, reference_type, reference_id)`
- **Wallet Debit**: `debit_kudos(user_id, amount, reference_type)`
- **Balance Check**: `get_wallet_balance(user_id)`
- **Transaction Audit**: Immutable ledger with timestamps

#### Push Notifications (core/push_notification_service.py)
- **Provider**: Expo Notifications
- **Device Registration**: Via DeviceToken model
- **Notification Types**: Event reminders, project feedback, milestone achievements

### Database Models (72+ Entities)

#### User Management Core

**User** (Base identity)
- `id`, `email`, `phone`, `password_hash`
- `google_id`, `referral_code`, `referral_parent_id`
- `created_at`, `updated_at`, `soft_deleted_at` (compliant deletion)
- `is_verified` (email/phone verified)

**Admin**, **Student**, **Faculty**, **VVDCoordinator**, **VVDPartner**, **ProjectApprover**, **ChannelManager**
- Each extends User with role-specific fields
- One-to-one relationship with User

#### Educational Content

**Institute**
- Name, description, location (lat/lon), contact
- Verification status, finance configuration
- Faculty relationships

**Course**
- Name, description, fee structure
- Razorpay plan integration for recurring payments
- CourseSubject mappings

**CourseSubject**
- Links Course → Subject
- Enables course curricula definition

**Subject**
- Name, description, faculty assignments
- SubjectSession (live classes)
- SubjectMaterial (resources)

**StudentSubjectEnrollment**
- Student → Subject relationship
- Tracks enrollment status, progress

**CourseEnrollment**
- Student → Course relationship
- Payment reference, completion status

#### Events System

**Event**
- Title, description, dates (start, end, registration window)
- Venue (in_person/online/hybrid), location
- EventTicketTier (pricing tiers)
- EventAdmin (creator/manager)

**EventTicket**
- Issued ticket records
- Attendee info, QR code, PDF delivery status

**EventTicketTier**
- Quantity, price (paise), name
- Early bird discounts

**EventCoupon**
- Discount code, percentage/fixed amount
- Usage limits, expiry, application conditions

**EventCheckIn**
- Attendance tracking via QR scan

**EventReferralConfig**
- Referral incentive per event

#### Hustle (Career Development)

**HustleRoadmap**
- Career path name, goal description
- Gemini-generated or manual creation

**HustleTask**
- Milestones within roadmap (ordered by task_order)
- Learning objectives, resource links
- Gemini-enriched content

**HustleStudentTaskProgress**
- Tracks completion status per student
- Timestamps for achievement dates

**HustleAIProject**
- Auto-generated capstone projects
- Triggered at milestone boundaries
- Gemini-created project descriptions

**HustleStudentAIProjectSubmission**
- Project code/document submission
- Approval status, feedback

**HustleResume**
- Student resume/profile
- Skills, experience, achievements
- Gemini-summarized strength scores

**HustlePayment**
- Subscription records (monthly/yearly)
- Razorpay integration

**HustleRanking**
- Leaderboards by College/Department
- Score aggregation

#### Payments & Billing

**Payment** (Universal transaction log)
- Polymorphic reference: `payment_for` (enum) + `reference_id` (UUID)
- References CourseEnrollment, HustlePayment, EventTicket, MonthlyFeeRecord
- Status: initiated, pending, captured, failed, refunded
- Razorpay order/payment ID

**MonthlyFeeRecord**
- Recurring course fees (1st of month)
- Course → Student relationship
- Payment tracking

**FeeTransaction**
- Individual fee payment attempts
- Status and error tracking

**Settlement**
- Institute/faculty payouts
- RazorpayX disbursement tracking

#### Kudos Reward System

**KudosWallet**
- `balance` (current), `lifetime_earned`, `lifetime_spent`
- Unique per user

**KudosTransaction**
- Immutable ledger: credit/debit
- `reference_type` (quiz_win, referral, course_purchase, etc.)
- `reference_id` (UUID to specific event)
- Timestamps, amounts

**KudosRewardRule**
- `action_type`, `reward_amount`
- Conditions for earning (e.g., quiz_win > ₹100 score)

**KudosRedemption**
- Redemption requests against partner items
- Status: pending, approved, rejected
- Fulfillment tracking

**VVDPartner**
- Partner organization for Kudos items
- Redemption catalog integration

#### Communication & Support

**Chat**
- User-to-user or User-to-Support messaging
- Message content, timestamps

**SupportTicket**
- Issue category, description, attachments
- Status: open, in_progress, resolved, closed
- Assignment to support agents

**Feedback**
- User satisfaction surveys
- Rating, comments

#### Miscellaneous

**OTP**
- Email/SMS one-time passwords
- 6-digit codes, 5-minute expiry
- Verification tracking

**DeviceToken**
- Push notification registration
- Expo token per device

**CareerRole**
- Job titles/roles for recommendations
- Skills mapping

**Referral**
- User referral program tracking
- Rewards for referring

**CollegeCatalog**
- External college directory
- Integration with Hustle college assignments

### Module Structure (16+ Feature Modules)

#### Admin Module (`modules/admin/`)
- CRUD for users, institutes, courses
- Admin invitation flow
- Mass operations for setup

#### Auth Module (`modules/auth/`)
- Email/phone registration
- Google OAuth verification (multiple client IDs)
- Email/password login
- JWT token management
- OTP delivery and verification
- Password reset

#### Events Module (`modules/events/`)
- Event CRUD (admin only)
- Ticket tier management
- Coupon creation and validation
- Ticket purchase with Razorpay
- Payment verification webhook
- Check-in system (QR codes)
- PDF ticket generation
- Referral mechanics

#### Hustle Module (`modules/hustle/`)

**Admin Sub-routes** (`routers/admin_courses.py`):
- Create/update roadmaps
- Create/update tasks
- Create/update courses
- Assign Hustle colleges

**Student Sub-routes** (`routers/student_tasks.py`):
- List enrolled roadmaps
- Get task details
- Mark tasks complete
- Track progress

**Project Sub-routes** (`routers/student_projects.py`):
- List available AI projects
- Submit project code
- Get feedback

**Profile Sub-routes** (`routers/student_profile.py`):
- Get/update resume
- Student profile data

**Payment Sub-routes** (`routers/student_payments.py`):
- Subscribe to Hustle (monthly/yearly)
- Verify subscription payment
- Get subscription status

**Services**:
- `lms_service.py`: Roadmap/task queries
- `payment_service.py`: Subscription verification
- `ranking_service.py`: Leaderboard calculations

#### Payments Module (`modules/payments/`)
- Razorpay webhook verification
- Payment status tracking
- Signature verification with error handling
- Row locking during verification (SELECT FOR UPDATE)
- Payment state machine

#### Kudos Module (`modules/kudos/`)
- Wallet initialization (auto on first credit)
- Earn Kudos (quizzes, referrals, purchases)
- Debit Kudos (redemptions)
- Transaction history
- Redemption management
- Partner integration

#### Student Module (`modules/student/`)
- Student profile (name, phone, location, bio)
- Institute/subject browsing
- Course purchases
- Enrollment management
- Fee overview

#### Faculty Module (`modules/faculty/`)
- Faculty profile
- Subject assignments
- Class session management
- Material uploads

#### Other Modules

| Module | Purpose |
|--------|---------|
| `catalog/` | College/subject discovery |
| `coordinator/` | Regional coordinator management |
| `institute/` | Institute profiles, verification |
| `institute_requests/` | Institute onboarding workflow |
| `channel_manager/` | Event organizer endpoints |
| `public/` | Public discovery endpoints |
| `onboarding/` | Multi-role registration flows |
| `quizzes/` | Quiz creation, attempts |
| `ranking/` | Student rankings |
| `referral/` | Referral program logic |
| `resume/` | Resume CRUD |
| `settlements/` | Finance payouts |
| `support/` | Support tickets |
| `uploads/` | S3 presigned URLs |
| `vvd_partner/` | Partner integrations |
| `webhooks/` | Razorpay callbacks |

---

## 5. Frontend (vvd-frontend)

### Technology Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | Next.js 14+ (App Router) |
| **Language** | TypeScript 5.0+ |
| **Build Tool** | Turbopack + Standalone Output |
| **Styling** | Tailwind CSS + Custom Design System |
| **UI Library** | shadcn/ui + Radix UI |
| **Icons** | Material Symbols, Lucide React, Hugeicons |
| **State** | React Query (TanStack Query) |
| **Forms** | React Hook Form + resolvers |
| **HTTP** | Axios |
| **Maps** | Leaflet.js |
| **Payments** | Razorpay SDK |
| **Analytics** | Microsoft Clarity, Meta Pixel |
| **Container** | Docker (multi-stage build) |

### Directory Structure

```
vvd-frontend/
├── next.config.ts                  # Build config, headers, CORS
├── tsconfig.json                   # TypeScript configuration
├── tailwind.config.ts              # Tailwind customization
├── postcss.config.mjs              # PostCSS plugins
├── components.json                 # shadcn/ui config
├── eslint.config.mjs               # Linting rules
├── package.json                    # Dependencies, scripts
├── Dockerfile                      # Multi-stage build
├── .env.example                    # Environment template
│
├── app/                            # Next.js App Router
│   ├── layout.tsx                  # Root layout, providers
│   ├── page.tsx                    # Home page
│   │
│   ├── api/                        # Server-side API proxies
│   │   ├── auth/[...path]/         # Auth proxy routes
│   │   ├── student/[...path]/      # Student API proxy
│   │   ├── events/[...path]/       # Events API proxy
│   │   ├── quizzes/[...path]/      # Quizzes API proxy
│   │   ├── hustle/[...path]/       # Hustle API proxy
│   │   └── onboard/[...path]/      # Onboarding proxy
│   │
│   ├── (tabs)/                     # Student main app (tab layout)
│   │   ├── page.tsx                # Home tab
│   │   ├── discover/               # Course discovery
│   │   ├── [subject-id]/           # Subject detail
│   │   ├── enrolled/               # My enrollments
│   │   ├── student-profile/        # Profile
│   │   ├── kudos/                  # Rewards wallet
│   │   └── layout.tsx              # Tab bar navigation
│   │
│   ├── (live)/                     # Live class browsing
│   ├── (hustle)/                   # Hustle module
│   │   ├── my-roadmap/
│   │   ├── projects/
│   │   ├── resume/
│   │   └── layout.tsx
│   │
│   ├── admin/                      # Admin dashboard
│   │   ├── users/
│   │   ├── institutes/
│   │   ├── courses/
│   │   └── events/
│   │
│   ├── careers/                    # Job opportunities
│   ├── community/                  # Community features
│   ├── contact/                    # Contact page
│   ├── institutes/                 # Institute browsing
│   ├── kudos/                      # Kudos browsing
│   ├── login/                      # Login flow
│   ├── login-admin/                # Admin login
│   ├── login-faculty/              # Faculty login
│   ├── login-partner/              # Partner login
│   ├── login-coordinator/          # Coordinator login
│   ├── login-channel-manager/      # Event organizer login
│   ├── privacy-policy/             # Legal pages
│   ├── terms/
│   └── arena/                      # Social/competitive features
│
├── components/                     # Reusable React components
│   ├── account/                    # Profile, settings, account
│   ├── analytics/                  # Analytics components
│   ├── auth/                       # Auth flows, modals
│   ├── chat/                       # Messaging UI
│   ├── coordinator/                # Coordinator dashboard
│   ├── events/                     # Event cards, detail, forms
│   ├── faculty/                    # Faculty profile, management
│   ├── hustle/                     # Roadmap, task, project UI
│   ├── hustle-ui/                  # Hustle-specific reusable UI
│   ├── institute/                  # Institute cards, detail
│   ├── map/                        # Location maps
│   ├── onboarding/                 # Registration flows
│   ├── partner/                    # Partner/ally UI
│   ├── public/                     # Public browsing
│   ├── student/                    # Student dashboard
│   ├── super_admin/                # Admin panel
│   └── ui/                         # Base UI library (30+ components)
│       ├── button.tsx
│       ├── input.tsx
│       ├── card.tsx
│       ├── dialog.tsx
│       ├── form.tsx
│       ├── table.tsx
│       └── ... (20+ more primitives)
│
├── lib/                            # Utilities and hooks
│   ├── api/                        # API clients
│   │   ├── student.ts              # Student endpoints
│   │   ├── events.ts               # Events endpoints
│   │   ├── faculty.ts              # Faculty endpoints
│   │   ├── partner.ts              # Partner endpoints
│   │   └── ... (more clients)
│   │
│   ├── auth/                       # Authentication
│   │   ├── auth-context.tsx        # Auth state provider
│   │   ├── jwt-utils.ts            # Token management
│   │   └── google-auth.ts          # Google OAuth helpers
│   │
│   ├── hooks/                      # Custom React hooks
│   │   ├── useAuth.ts              # Auth context hook
│   │   ├── useStudent.ts           # Student data hook
│   │   ├── useEvents.ts            # Events data hook
│   │   └── ... (more hooks)
│   │
│   ├── types/                      # TypeScript types
│   │   ├── student.ts
│   │   ├── event.ts
│   │   ├── payment.ts
│   │   └── ... (comprehensive type definitions)
│   │
│   ├── utils.ts                    # String formatting, dates
│   ├── constants.ts                # Platform constants, URLs
│   └── config.ts                   # Environment configuration
│
└── public/                         # Static assets
    ├── images/
    ├── fonts/
    └── icons/
```

### Frontend Stack & Structure

- **Framework**: Next.js 14+ (App Router) + TypeScript + Tailwind CSS
- **UI**: shadcn/ui + Radix UI components, custom design system
- **State**: React Query for server state, context for auth
- **Forms**: React Hook Form + resolvers
- **Key Sections**: Auth, Student tabs, Hustle module, Admin dashboard, Events, Institute browsing
- **API**: Axios client with JWT interceptors, retry logic
- **Deploy**: Docker multi-stage build, standalone output

### Technology Stack Summary

| Component | Tech |
|-----------|------|
| Backend | Python 3.11, FastAPI, SQLAlchemy 2.0, asyncpg |
| Frontend | Next.js 14+, TypeScript, Tailwind, shadcn/ui |
| Mobile | Expo 55, React Native, Expo Router |
| Database | PostgreSQL 12+ |
| Payments | Razorpay |
| Storage | AWS S3 |
| AI | Google Gemini |
| Infra | Docker, Traefik, Let's Encrypt |

---

## 6. Mobile (vvd-mobile)

**Framework**: Expo 55 + React Native 0.83 + TypeScript  
**Navigation**: Expo Router with role-based tab navigation  
**State**: React Query, AsyncStorage for local data  
**Payments**: React Native Razorpay SDK  
**Features**: Camera/QR scanning, image upload, push notifications, offline support

**Key Modules**: Authentication flows, student/faculty/partner tabs, project submissions, profile management

---

## 7. Database & Models

**ORM**: SQLAlchemy 2.0 async + asyncpg  
**Database**: PostgreSQL 12+  
**Migrations**: Alembic  

**72+ Models** organized by domain:
- **Users**: User, Admin, Student, Faculty, VVDCoordinator, VVDPartner, ProjectApprover, ChannelManager
- **Learning**: Institute, Course, Subject, StudentSubjectEnrollment, CourseEnrollment, SubjectSession
- **Events**: Event, EventTicket, EventTicketTier, EventCoupon, EventCheckIn, EventAdmin
- **Hustle**: HustleRoadmap, HustleTask, HustleStudentTaskProgress, HustleAIProject, HustleResume, HustlePayment, HustleRanking
- **Payments**: Payment (polymorphic), MonthlyFeeRecord, Settlement, FeeTransaction
- **Rewards**: KudosWallet, KudosTransaction, KudosRewardRule, KudosRedemption
- **Misc**: Chat, SupportTicket, Feedback, OTP, DeviceToken, Referral, CareerRole

**Key Relationships**:
```
User (1) → Student/Faculty/Admin/Partner/Coordinator/Approver/ChannelManager (0..1)
Institute (1) ← many Course, Faculty
Course (1) ← many CourseSubject → (1) Subject
Subject (1) ← many StudentSubjectEnrollment → (many) Student
Event (1) ← many EventTicket, EventTicketTier, EventCoupon
HustleRoadmap (1) ← many HustleTask
Payment (polymorphic) → CourseEnrollment | EventTicket | HustlePayment | MonthlyFeeRecord
KudosWallet (1) ← (1) User → many KudosTransaction
```

---

## 8. API Structure & Integration Points

**API Patterns**: REST JSON endpoints with JWT Bearer token authentication

**Key Endpoint Groups**:

| Group | Key Routes |
|-------|-----------|
| **Auth** | POST /auth/register, /auth/login, /auth/google, /auth/refresh |
| **Student** | GET /student/me, GET /student/institutes, POST /student/courses/{id}/buy |
| **Events** | GET/POST /events/admin, GET /events, POST /events/{id}/buy |
| **Hustle** | GET /hustle/roadmaps, PATCH /hustle/tasks/{id}/complete, POST /hustle/subscribe |
| **Kudos** | GET /kudos/wallet, POST /kudos/redeem, GET /kudos/rules |
| **Public** | GET /public/discover, GET /public/institutes, GET /public/kudos/info |
| **Webhooks** | POST /webhooks/razorpay/payment, /webhooks/razorpay/refund |

**Frontend Proxies** (Next.js API routes):
```
/api/auth/* → backend /api/v1/auth/*
/api/student/* → backend /api/v1/student/*
/api/events/* → backend /api/v1/events/*
/api/hustle/* → backend /api/v1/hustle/*
```

---

## 9. External Integrations

| Integration | Purpose | Key Function |
|-------------|---------|--------------|
| **Razorpay** | Payment processing | Order creation, signature verification, webhooks, RazorpayX payouts |
| **Google OAuth** | Authentication | Multi-client ID support (web, mobile, desktop), ID token verification |
| **AWS S3** | File storage | Presigned URLs for uploads/downloads, role-based path organization |
| **Google Gemini AI** | Content generation | Roadmap generation, task enrichment, project creation, resume summaries |
| **SMTP/Email** | Communications | OTP delivery, event confirmations, support notifications, PDF attachments |
| **Expo Notifications** | Push alerts | Device token registration, event reminders, achievement notifications |
| **Redis** (optional) | Caching | Rate limiting, session caching, job queues |

---

## 10. Security & Authentication

**Password Hashing**: Argon2id (memory-hard, GPU-resistant) with cost factors: time=3, memory=64MB, parallelism=4

**JWT Tokens**: HS256 algorithm, access token (60 min), refresh token (30 days)

**API Security**: CORS whitelist, security headers (X-Content-Type-Options, X-Request-ID), JWT Bearer auth, role-based guards

**Payment Security**: Razorpay webhook signature verification (HMAC-SHA256), constant-time comparison, SELECT FOR UPDATE row locking, idempotency via reference tracking

**Data Privacy**: Soft deletion for GDPR compliance, PII purging on account deletion, 30-day recovery window

**Authorization**: Role-based access control via dependency injection (`require_student()`, `require_faculty()`, etc.)

---

## 11. Deployment & Infrastructure

**Containerization**: Docker multi-stage builds for backend (Python 3.11-slim) and frontend (Node 22-bookworm)

**Orchestration**: Docker Compose for local dev, Traefik reverse proxy for production

**SSL/TLS**: Let's Encrypt with auto-renewal

**Database**: PostgreSQL 12+ (cloud-hosted), asyncpg async driver, PgBouncer for connection pooling

**Reverse Proxy**: Traefik with domain routing, load balancing, health checks

**CI/CD**: GitHub Actions for automated build, push to registry, SSH deploy, post-deploy healthcheck

**Scaling**: Horizontal scaling via Traefik load balancing, Redis for caching, CDN for static assets

---

## 12. Development Workflow

**Backend**:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Configure DATABASE_URL, API keys
alembic upgrade heads
python -m uvicorn main:app --reload
```

**Frontend**:
```bash
npm install && npm run dev  # http://localhost:3000
npx tsc --noEmit           # Type check
npm run lint --fix         # Fix linting issues
npm run build              # Production build
```

**Mobile**:
```bash
npm install && npm start   # Start Expo server
npm run android            # Android emulator
npm run ios                # iOS simulator
npm run typecheck          # Type check
```

**Database**:
```bash
alembic revision --autogenerate -m "description"  # Create migration
alembic upgrade heads                              # Apply migrations
alembic downgrade -1                               # Rollback
pytest                                             # Run tests
```

---

## 13. Key Architectural Decisions & Patterns

**Design Patterns**:
- **Service Layer**: Business logic in modules/*/service.py
- **Repository Pattern**: SQLAlchemy as query builder
- **Dependency Injection**: FastAPI Depends() for DB sessions, auth guards
- **Strategy Pattern**: Email providers (SMTP, console, disabled)
- **Observer Pattern**: Webhooks for async payment processing
- **Polymorphic Reference**: Payment model → CourseEnrollment | EventTicket | HustlePayment | MonthlyFeeRecord
- **Soft Delete Pattern**: GDPR-compliant user deletion with recovery window
- **Timestamp Mixin**: Automatic created_at/updated_at tracking
- **Async-First**: Non-blocking I/O via SQLAlchemy 2.0 + asyncpg

**Key Decisions**:
- Monolithic FastAPI backend with modular organization (scales to microservices if needed)
- Stateless APIs for horizontal scaling
- Frontend API gateway via Next.js for CORS elimination and retry logic
- Polymorphic payments to support multiple transaction types flexibly
- Soft deletion for data protection and compliance

---

## 14. Notable Features & Systems

**Hustle Module**: AI-powered career development with roadmaps, milestone tracking, auto-generated projects, resume building, subscriptions (monthly/yearly), leaderboards

**Kudos System**: Gamified rewards (earn via quizzes, referrals, purchases; redeem at partners), wallet per user, immutable transaction ledger

**Event Management**: Complete lifecycle (creation, tiered pricing, coupons, QR check-in, PDF tickets, referral mechanics)

**Multi-Role Platform**: 8 distinct user roles with separate permissions (student, faculty, admin, coordinator, partner, approver, channel manager)

**Payment Hardening**: Idempotent payment flows with webhook verification, row locking, reference tracking, retry logic

**Location-Based Discovery**: Geo-proximity features for institutes, faculty, and events

**AI Integration**: Gemini powers roadmap generation, task enrichment, project creation, resume summaries

---

## 15. Current Development Status

## 15. Current Development Status

**✅ Completed**: Auth, multi-role access, course enrollment, event ticketing, Hustle module, Kudos rewards, S3 uploads, payment verification, email/notifications, 72+ models

**🔄 In Progress**: Guest sessions, public APIs, mobile payment hardening, quizzes, faculty live sessions

**⚠️ Known Issues**: Multiple Alembic migration heads (needs consolidation), frontend TypeScript linting errors

**📋 Planned**: Partner APIs, advanced analytics, bulk operations, ML recommendations

---

## Quick Reference

**Key Files**:
- Backend config: `core/config.py`
- Database setup: `core/database.py`
- Models: `models/`
- Modules: `modules/` (16+ features)
- Frontend: `app/` (App Router), `lib/api/` (API clients)
- Mobile: `app/` (Expo Router), `lib/`

**Environment**:
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db
SECRET_KEY=your_secret
GOOGLE_CLIENT_ID_WEB=xxxxx
RAZORPAY_KEY_ID=xxxxx
AWS_ACCESS_KEY_ID=xxxxx
GEMINI_API_KEY=xxxxx
EMAIL_PROVIDER=smtp
```

**Common Commands**:
```bash
# Backend
python -m uvicorn main:app --reload
alembic upgrade heads

# Frontend
npm run dev

# Mobile
npm start

# Tests
pytest
```

---

**Document Version**: 2.0 (Condensed)  
**Last Updated**: June 6, 2026  
**Status**: Maintained by VVD Development Team
