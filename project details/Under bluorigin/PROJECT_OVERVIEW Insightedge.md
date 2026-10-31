# InsightEdge - Project Overview

## Problem Statement
Businesses need real-time competitive intelligence to monitor competitors, track market changes, analyze social media presence, and generate actionable insights - but existing tools are fragmented, expensive, and lack AI-powered analysis.

## Solution
InsightEdge is a comprehensive Competitive Intelligence SaaS platform that provides automated monitoring, data aggregation, and AI-powered analysis of competitors across multiple channels (websites, social media, Instagram) with structured reporting and alerts.

---

## Core Technologies

### Backend Stack
- **Framework**: FastAPI (Python 3.11+) - Async REST API
- **Database**: Supabase (PostgreSQL + Auth + Storage)
- **Authentication**: Supabase Auth with JWT tokens
- **Background Jobs**: APScheduler for periodic tasks
- **Caching**: Redis for sessions and job queues
- **AI**: OpenAI GPT-4 for report generation
- **Web Scraping**: 
  - Instaloader for Instagram
  - Playwright for LinkedIn
  - BeautifulSoup + LXML for website monitoring
  - changedetection.io integration
- **Payments**: Stripe for billing/subscriptions
- **Storage**: AWS S3 / Cloudflare R2
- **Logging**: Structlog (JSON structured logs)
- **Rate Limiting**: SlowAPI
- **Deployment**: Railway (production)

### Frontend Stack
- **Framework**: Next.js 15.2.4 (React 19, App Router)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 4.1.9
- **UI Components**: Radix UI primitives
- **Forms**: React Hook Form + Zod validation
- **Charts**: Recharts
- **State**: React Context API
- **HTTP**: Fetch API
- **Deployment**: Vercel-ready

### Third-Party Integrations
- **changedetection.io**: Website change detection engine
- **Instaloader**: Instagram profile scraping
- **Playwright**: Browser automation for LinkedIn
- **Stripe**: Payment processing
- **OpenAI**: GPT-4 for AI insights
- **Twitter API**: Social media monitoring

---

## Architecture Overview

### Multi-Tenant Design
- **Organizations**: Teams with owner/admin/member/viewer roles
- **Memberships**: Many-to-many user-organization relationships
- **Row Level Security (RLS)**: Database-level isolation per organization
- **Per-user JWT authentication** via Supabase

### Database Schema
**Core Tables**:
- `organizations`, `memberships` - Multi-tenancy
- `targets` - Competitors/suppliers to track
- `reports`, `report_sections` - Intelligence reports
- `ai_reports` - Generated AI reports with full content
- `website_monitors`, `website_snapshots`, `website_changes` - Website monitoring
- `instagram_profiles`, `instagram_profile_snapshots`, `instagram_posts` - Instagram data
- `linkedin_profiles`, `linkedin_posts`, `linkedin_scrape_jobs` - LinkedIn scraping
- `provider_runs` - Data provider execution audit trail
- `usage_events` - Billing and quotas tracking
- `feature_flags` - Admin feature controls

### Service Layer Architecture
**Backend Services** (`app/services/`):
- `billing.py` - Stripe integration, subscriptions
- `openai_service.py` - GPT-4 report generation with structured schemas
- `instagram_insights.py` - Instaloader integration
- `linkedin/` - Playwright scraper, session management, proxy rotation
- `website_monitoring/` - Fetcher, differ, monitor service, background worker
- `changedetection.py` - changedetection.io API integration
- `scheduler.py` - Background job scheduler

---

## Key Features

### 1. Website Monitoring
- **Monitor competitor websites** for content changes
- **CSS selector filtering** for targeted monitoring
- **Automated periodic checks** (configurable intervals)
- **Change detection** with line-by-line diffs
- **Price change detection** with regex patterns
- **Significance scoring** (0-100)
- **HTML diff visualization**
- **Snapshot history** with timestamps
- **Manual check triggers**
- **Alert configuration** (coming soon)

**Tech**: BeautifulSoup, LXML, APScheduler, changedetection.io integration

### 2. Instagram Insights
- **No login required** - Works with public profiles
- **Profile analytics**: Followers, following, posts count, bio
- **Engagement metrics**: Avg likes, avg comments, engagement rate
- **Recent posts analysis** (configurable limit)
- **Video view tracking**
- **Historical snapshots** for trend analysis
- **Profile comparison** (multiple accounts)
- **Fast Instaloader-based** scraping

**Tech**: Instaloader 4.13+, async Python

### 3. LinkedIn Insights
- **Playwright-based scraping** with stealth techniques
- **Human-like scrolling** and interaction patterns
- **Up to 50 posts per profile**
- **Engagement metrics**: Reactions, comments, reposts
- **Media URL extraction**
- **Session management** with persistent cookies
- **Proxy rotation** with health tracking
- **Redis/RQ async job queue**
- **Job status tracking** with retries

**Tech**: Playwright, Redis, RQ worker system

### 4. Twitter/X Monitoring
- **Twitter API v2 integration**
- **Recent tweets** fetching (up to 10)
- **Public metrics**: Likes, retweets, replies, quotes
- **5-minute caching** to reduce rate limits
- **Rate limit handling** with cached fallbacks

**Tech**: Twitter API v2, httpx async client

### 5. AI-Powered Reports
- **Competitor Reports**: Automated analysis of website changes
  - Executive summary with sentiment
  - Key metrics extraction
  - Threat scores (0-100)
  - Insight sections with severity
  - Actionable recommendations with priority/timeframe
  - Chart data for visualizations
- **Instagram Reports**: Social media performance analysis
  - Profile comparison
  - Engagement trends
  - Content strategy insights
- **Structured JSON output** with strict schemas
- **Auto-save to database** after generation
- **Pagination and filtering**
- **Copy/download functionality**

**Tech**: OpenAI GPT-4 with JSON schema validation

### 6. Authentication & Authorization
- **Supabase Auth** for user management
- **JWT token-based** authentication
- **Access + Refresh tokens**
- **Role-Based Access Control (RBAC)**
- **Password reset** functionality
- **Email verification**
- **Session management**

### 7. Billing & Subscriptions
- **Stripe integration** for payments
- **Multiple subscription tiers** (Free, Pro, Enterprise)
- **Usage-based quotas**
- **Checkout sessions** for upgrades
- **Invoice management**
- **Webhook handling** for events
- **Customer portal** integration

### 8. Admin Panel
- **User management** (list, view, block/unblock)
- **Analytics dashboard**
- **Feature flags** control
- **Usage statistics**
- **Admin authentication** with separate JWT

---

## API Structure

### Endpoints (`/api/v1/`)
- **Auth**: `/auth/` - Login, signup, logout, token refresh, password reset
- **Users**: `/users/` - Profile management, user details
- **Billing**: `/billing/` - Plans, subscriptions, invoices, checkout
- **Social Media**: `/socials/` - Twitter data fetching
- **Competitor Monitor**: `/competitor-monitor/` - CRUD monitors, check, history, stats
- **Instagram Insights**: `/instagram-insights/` - Profile analysis, comparison, health
- **Instagram Scraper**: `/instagram/` - Legacy scraper endpoint
- **Social Reports**: `/social-reports/` - Generate social media reports
- **Reports**: `/reports/` - Generate AI reports, list saved reports, view reports
- **Admin**: `/admin/` - User management, analytics, feature flags

### Response Format
```json
{
  "success": true,
  "data": {...},
  "request_id": "uuid",
  "error": null
}
```

---

## Frontend Structure

### Pages (`app/`)
- `/` - Dashboard with stats overview
- `/landing` - Public landing page
- `/auth/signin`, `/auth/signup` - Authentication
- `/settings` - User profile settings
- `/reports` - Generate and view AI reports (tabbed interface)
- `/web-monitoring` - Website monitor management
- `/instagram-insights` - Instagram profile analysis
- `/twitter-insights` - Twitter monitoring
- `/billing` - Subscription management
- `/admin` - Admin panel (users, analytics)

### Components (`components/`)
- `layout/` - Main layout, navigation, sidebar
- `ui/` - Reusable Radix UI components (Button, Card, Dialog, etc.)
- `charts/` - Recharts-based visualization components
- `social/` - Social media-specific components

### Services (`lib/services/`)
- `monitoring.ts` - Website monitoring API calls
- `reports.ts` - AI reports API calls
- Type-safe API client with error handling

---

## Development Workflow

### Backend Setup
```bash
cd InsightEdgeBackend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env  # Configure environment
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd InsightEdgeFrontend
pnpm install
pnpm dev  # Runs on port 3000
```

### Database Migrations
Run SQL files in `InsightEdgeBackend/migrations/` in Supabase SQL Editor

---

## Key Differentiators

1. **Unified Platform**: Single dashboard for website, Instagram, LinkedIn, Twitter monitoring
2. **AI-Powered Insights**: GPT-4 analysis with structured, actionable reports
3. **No Login Required**: Instagram insights work with public profiles
4. **Real-Time Monitoring**: Automated background workers with configurable intervals
5. **Multi-Tenant SaaS**: Organization-based isolation with RBAC
6. **Production-Ready**: Structured logging, rate limiting, error handling, health checks
7. **Open Integration**: changedetection.io integration for advanced website monitoring

---

## Production Deployment

### Backend
- **Platform**: Railway
- **Environment**: Production mode with TrustedHostMiddleware
- **URL**: `insightedgebackend-production-537b.up.railway.app`
- **Database**: Supabase cloud PostgreSQL
- **Logging**: JSON structured logs via structlog

### Frontend
- **Platform**: Vercel (recommended)
- **Build**: `next build`
- **Environment**: Production Next.js app

---

## Security Features

- **JWT Authentication** with token expiration
- **Row Level Security (RLS)** in PostgreSQL
- **CORS** middleware with configurable origins
- **Rate Limiting** on API endpoints
- **Environment variable** protection
- **SQL injection** prevention via parameterized queries
- **XSS protection** via React's built-in escaping
- **HTTPS** enforcement in production
- **Stripe webhook signature** verification

---

## Performance Optimizations

- **Redis caching** for frequently accessed data
- **Database indexes** on foreign keys and queries
- **Async/await** throughout backend
- **Connection pooling** via Supabase client
- **Lazy loading** of OpenAI client
- **5-minute Twitter API cache**
- **Parallel API calls** in frontend
- **React Server Components** in Next.js
- **Semaphore-based** concurrent job limits

---

## Future Enhancements (Documented)

- LinkedIn insights frontend integration
- Alert notifications via email/webhook
- Pricing page with Stripe checkout
- Advanced filtering and search
- Report scheduling
- Team collaboration features
- API webhooks for integrations
- Mobile app (React Native)

---

## Project Metrics

**Backend**:
- 15+ API endpoint routers
- 20+ database tables
- 8+ background services
- 100+ API routes

**Frontend**:
- 10+ pages
- 50+ UI components
- 5+ feature modules
- Full TypeScript coverage

**Integrations**:
- 7 third-party services
- 3 social media platforms
- 2 payment processors
- 1 AI provider

---

## Documentation Files

- `README.md` - Backend setup guide
- `INTEGRATION_SUMMARY.md` - Website monitoring implementation
- `INSTAGRAM_INSIGHTS_README.md` - Instagram feature guide
- `LINKEDIN_INSIGHTS_IMPLEMENTATION.md` - LinkedIn scraping details
- `REPORTS_STORAGE_IMPLEMENTATION.md` - AI reports storage
- `WEBSITE_MONITORING_SIMPLIFIED.md` - Simplified monitoring guide
- `CHANGE_DETECTION_*.md` - changedetection.io integration docs
- `REPORTS_TESTING_GUIDE.md` - Testing guidelines

---

## File Structure Summary

```
InsightEdge/
├── InsightEdgeBackend/          # FastAPI backend
│   ├── app/
│   │   ├── api/v1/endpoints/    # API routes
│   │   ├── core/                # Config, database
│   │   ├── models/              # Pydantic models
│   │   ├── services/            # Business logic
│   │   └── main.py              # App entry point
│   ├── migrations/              # SQL migrations
│   ├── requirements.txt         # Python dependencies
│   └── supabase-schema.sql      # Database schema
├── InsightEdgeFrontend/         # Next.js frontend
│   ├── app/                     # Pages (App Router)
│   ├── components/              # React components
│   ├── lib/                     # Utilities, API clients
│   └── package.json             # Node dependencies
└── changedetection.io-master/   # Integrated monitoring engine
```
