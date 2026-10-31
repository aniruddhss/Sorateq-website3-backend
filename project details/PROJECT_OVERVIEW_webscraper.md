# BEN WebScraper - Project Overview

## Problem
E-commerce businesses and market analysts need to identify payment infrastructure (gateways, processors, platforms) across multiple websites efficiently without manual inspection.

## Solution
Full-stack web application that automates payment detection through bulk CSV processing with intelligent web scraping and real-time progress tracking.

---

## Core Functionality

### Input
- CSV files containing website URLs
- Auto-detects URL columns (url, website, domain)
- In-browser CSV editing (add/remove rows/columns, bulk updates)
- Drag-and-drop upload interface

### Processing
- Multi-page analysis (homepage, checkout, contact pages)
- Concurrent processing (8 workers, configurable)
- Request throttling (0.8s delay, SSL verification disabled)
- Automatic retry logic (2 retries with exponential backoff)

### Output
- Payment gateways detected (20+ including Stripe, Razorpay, PayPal, Square)
- Payment processors identified (Visa, Mastercard, Amex, Discover, JCB, RuPay, UnionPay, Maestro, Diners)
- E-commerce platforms recognized (40+ including Shopify, WooCommerce, Magento, BigCommerce)
- Frontend/backend frameworks detected (React, Vue, Angular, Next.js, Laravel, Django)
- Contact information extracted (emails, phone numbers)
- Domain authority estimation
- Downloadable CSV with all results

---

## Technology Stack

### Frontend
- **Framework**: Next.js 15.5.5 (App Router)
- **Language**: TypeScript 5.x
- **UI Library**: React 19.1.0
- **Styling**: Tailwind CSS 4.x
- **Authentication**: NextAuth.js 4.24.11 (Google OAuth)
- **CSV Handling**: Papa Parse 5.5.3
- **File Upload**: React Dropzone 14.3.8
- **Notifications**: React Hot Toast 2.6.0
- **Icons**: Lucide React 0.546.0

### Backend
- **Framework**: FastAPI 0.104.0+
- **Server**: Uvicorn 0.24.0+ (ASGI)
- **Language**: Python 3.11+
- **HTTP Client**: Requests 2.31.0+
- **HTML Parsing**: BeautifulSoup4 4.12.0+ with lxml 4.9.0+
- **Data Processing**: Pandas 2.1.0+
- **Validation**: Pydantic 2.5.0+
- **Concurrency**: ThreadPoolExecutor (stdlib)

### Infrastructure
- **Deployment**: Render.com (separate frontend/backend services)
- **Storage**: In-memory (no database)
- **Communication**: REST API (HTTP/HTTPS)
- **File Transfer**: Multipart/form-data

---

## Architecture

### System Flow
```
User → Next.js Frontend → NextAuth Middleware → API Routes → FastAPI Backend → Target Websites
     ←  React UI      ←  Session Check     ←  JSON/CSV   ←  HTTP Requests  ←  HTML/JS/CSS
```

### Communication Pattern
1. Frontend validates and displays CSV data
2. User triggers processing
3. Next.js API validates session and forwards to FastAPI
4. FastAPI creates task, returns task_id
5. Frontend polls status endpoint every 3 seconds
6. Backend processes URLs concurrently (ThreadPoolExecutor)
7. Results streamed back with real-time progress
8. User downloads completed CSV

### Component Structure
- **Frontend**: `/ben-webscraper/` (Next.js app)
- **Backend**: `/ben-webscraper-backend/` (Python FastAPI)
- **Frontend Routes**:
  - `/` - Landing page
  - `/auth/signin` - Google OAuth login
  - `/dashboard` - Main CSV upload interface
  - `/api/process-csv` - CSV submission endpoint
  - `/api/status/[taskId]` - Progress polling endpoint
- **Backend Routes**:
  - `POST /upload-csv` - Accepts CSV, starts processing
  - `GET /status/{task_id}` - Returns task progress/results
  - `GET /health` - Health check endpoint

---

## Key Features

### 1. Authentication & Authorization
- Google OAuth 2.0 via NextAuth.js
- Admin-only access (whitelist via `ADMIN_EMAILS` env var)
- Session-based middleware protecting all routes except auth pages
- Automatic redirect to sign-in for unauthorized users

### 2. CSV Management
- Real-time parsing with validation
- Pagination (configurable rows per page)
- Column visibility controls
- Live editing (cell, row, column level)
- Add/remove rows and columns
- Bulk update operations
- Export edited data

### 3. Detection Engine
**Payment Gateways** (20+):
- Stripe, Razorpay, PayPal, PayU, Instamojo, Cashfree
- CCAvenue, Paytm, PhonePe, Google Pay, Square
- Authorize.net, Braintree, Mollie, Adyen, 2Checkout
- Shopify Payments, BigCommerce Payments

**Payment Processors** (10+):
- Visa, Mastercard, American Express, Discover
- Diners Club, JCB, Maestro, RuPay, UnionPay

**E-commerce Platforms** (40+):
- Shopify, WooCommerce, Magento, BigCommerce, Squarespace
- Wix, WordPress, Drupal, PrestaShop, OpenCart
- BigCartel, Volusion, 3DCart, Salesforce Commerce
- CommerceTools, Ecwid

**Tech Frameworks**:
- Frontend: React, Vue, Angular, Next.js, Gatsby, Svelte
- Backend: Laravel, Django, Flask, FastAPI, Express

### 4. Intelligent Scraping
- Multi-page analysis (homepage → checkout → contact)
- Pattern matching (signatures, meta tags, JS variables, HTML attributes)
- Confidence scoring for detections
- Contact extraction (emails, phone numbers)
- Domain authority estimation
- 5MB page size limit
- 20-second timeout per page
- SSL verification disabled for problematic sites
- User-Agent spoofing

### 5. Concurrent Processing
- ThreadPoolExecutor with 8 workers
- Rate limiting (0.8s delay between requests)
- In-memory task storage with progress tracking
- Maximum 100 results kept in memory
- Automatic truncation for large datasets
- Graceful error handling per URL

### 6. Real-time Progress
- Status polling every 3 seconds
- Progress percentage (0-100%)
- Processed/total URL counts
- Live result streaming
- Task states: pending, running, completed, failed, cancelled
- 2-hour maximum timeout

### 7. Error Handling
- Per-URL error isolation
- Retry logic with exponential backoff
- SSL certificate bypassing
- Request timeout handling
- Graceful degradation for failed pages
- Comprehensive logging

---

## Performance Characteristics

### Processing Times
- **10 URLs**: ~2-3 minutes
- **50 URLs**: ~8-10 minutes
- **99 URLs**: ~15-18 minutes

### Configuration Parameters
```python
workers = 8           # Concurrent threads
delay = 0.8          # Seconds between requests
timeout = 20         # Seconds per request
max_retries = 2      # Retry attempts
```

### Resource Limits
- CSV upload: 10MB max
- Page content: 5MB max
- Results in memory: 100 items max
- Task timeout: 2 hours
- SSL verification: Disabled

---

## Detection Methods

### Signature Matching
- String patterns in HTML/JS/CSS
- Domain references (cdn.stripe.com, checkout.razorpay.com)
- JavaScript library names (stripe.js, razorpay.js)
- API keys/tokens (pk_live_, rzp_live_)
- HTML attributes (data-stripe, data-paypal)
- CSS classes (stripe-button, paypal-checkout)

### Meta Tag Analysis
- Platform declarations (`<meta name="platform" content="shopify">`)
- Generator tags (`<meta name="generator" content="WordPress">`)
- Application names

### JavaScript Variable Detection
- Global objects (__NEXT_DATA__, Shopify, WooCommerce)
- Framework signatures (__VUE__, React, Angular)
- Configuration objects

### URL Pattern Detection
- Checkout pages (/checkout, /cart, /payment)
- Contact pages (/contact, /about)
- API endpoints
- CDN references

### Confidence Scoring
- Multiple detection methods increase confidence
- Weighted scoring based on signal strength
- Threshold-based classification

---

## Security & Access Control

### Authentication Flow
1. User clicks "Sign in with Google"
2. NextAuth.js redirects to Google OAuth
3. Google returns user profile
4. Email checked against ADMIN_EMAILS whitelist
5. JWT token issued and stored in session
6. Middleware validates session on protected routes

### Environment Variables
```env
# Frontend (.env.local)
GOOGLE_CLIENT_ID=<google-oauth-client-id>
GOOGLE_CLIENT_SECRET=<google-oauth-secret>
ADMIN_EMAILS=admin1@gmail.com,admin2@company.com
NEXTAUTH_SECRET=<random-secret>
NEXTAUTH_URL=<frontend-url>
BACKEND_API_URL=<backend-url>

# Backend
ALLOWED_ORIGINS=<frontend-url>
```

### Protected Routes
- All routes except `/auth/*` and `/api/auth/*` require authentication
- Middleware intercepts unauthorized requests
- Automatic redirect to sign-in page

---

## Data Flow

### Upload Phase
```
User → File Upload → Papa Parse → Validation → Display → Edit (optional) → Submit
```

### Processing Phase
```
Submit → Next.js API → FastAPI /upload-csv → Task Creation → Background Processing
                                                ↓
                                          ThreadPoolExecutor
                                                ↓
                                    [Worker 1] [Worker 2] ... [Worker 8]
                                                ↓
                                        Target Websites
                                                ↓
                                        Detection Engine
                                                ↓
                                        Results Storage
```

### Status Phase
```
Frontend (3s interval) → Next.js API → FastAPI /status/{task_id} → Task Status
                                                ↓
                                    Progress + Partial Results
```

### Download Phase
```
Task Complete → Frontend → Generate CSV → Download
```

---

## File Structure

```
ben-webscraper/
├── ben-webscraper/                    # Frontend (Next.js)
│   ├── src/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   ├── auth/[...nextauth]/route.ts    # OAuth handler
│   │   │   │   ├── process-csv/route.ts           # CSV submission
│   │   │   │   └── status/[taskId]/route.ts       # Status polling
│   │   │   ├── auth/signin/page.tsx               # Login UI
│   │   │   ├── dashboard/page.tsx                 # Main interface
│   │   │   ├── layout.tsx                         # Root layout
│   │   │   └── page.tsx                           # Landing page
│   │   ├── components/
│   │   │   ├── csv-uploader.tsx                   # Main component
│   │   │   ├── dashboard-layout.tsx               # Dashboard wrapper
│   │   │   └── providers.tsx                      # Context providers
│   │   ├── lib/auth.ts                            # Auth config
│   │   └── middleware.ts                          # Route protection
│   ├── public/sample-domains.csv
│   ├── package.json
│   ├── next.config.ts
│   └── tsconfig.json
│
└── ben-webscraper-backend/            # Backend (FastAPI)
    ├── main.py                        # Render entry point
    ├── simple_csv_api.py              # FastAPI app (576 lines)
    ├── payment_detector.py            # Detection logic (2776 lines)
    ├── start_csv_api.py               # Local startup
    ├── shutdown_api.py                # Graceful shutdown
    └── requirements.txt
```

---

## API Endpoints

### Frontend API Routes

#### POST `/api/process-csv`
- **Auth**: Required (session)
- **Input**: `{ headers: string[], rows: string[][], filename: string }`
- **Output**: `{ task_id, total_urls, status_url, estimated_time_minutes }`
- **Action**: Forwards CSV to backend, creates processing task

#### GET `/api/status/[taskId]`
- **Auth**: Required (session)
- **Input**: Task ID in URL
- **Output**: `{ status, progress, processed_urls, total_urls, results[], error_message }`
- **Action**: Polls backend for task status

### Backend API Routes

#### POST `/upload-csv`
- **Input**: Multipart form-data with CSV file
- **Query Params**: `workers`, `delay`, `timeout`
- **Output**: `{ task_id, total_urls, detected_url_column, status_url, estimated_time_minutes }`
- **Action**: Parses CSV, creates task, starts background processing

#### GET `/status/{task_id}`
- **Input**: Task ID in URL
- **Output**: `{ task_id, status, progress, processed_urls, total_urls, results[], completed_at }`
- **Action**: Returns current task state and results

#### GET `/health`
- **Output**: `{ status: "ok" }`
- **Action**: Health check for uptime monitoring

---

## Detection Capabilities Summary

| Category | Count | Examples |
|----------|-------|----------|
| Payment Gateways | 20+ | Stripe, Razorpay, PayPal, Square, Braintree |
| Payment Processors | 10+ | Visa, Mastercard, Amex, Discover, JCB, RuPay |
| E-commerce Platforms | 40+ | Shopify, WooCommerce, Magento, BigCommerce |
| Frontend Frameworks | 6 | React, Vue, Angular, Next.js, Gatsby, Svelte |
| Backend Frameworks | 5 | Laravel, Django, Flask, FastAPI, Express |

---

## Deployment

### Frontend (Render.com)
- **Type**: Web Service
- **Build**: `npm install && npm run build`
- **Start**: `npm start`
- **Port**: 3000
- **Environment**: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, ADMIN_EMAILS, NEXTAUTH_SECRET, NEXTAUTH_URL, BACKEND_API_URL

### Backend (Render.com)
- **Type**: Web Service
- **Build**: `pip install -r requirements.txt`
- **Start**: `uvicorn main:app --host 0.0.0.0 --port 8000`
- **Port**: 8000
- **Environment**: ALLOWED_ORIGINS

---

## Limitations

- **No Database**: In-memory storage, results lost on server restart
- **Memory Limits**: Max 100 results stored, older results truncated
- **Rate Limiting**: 0.8s delay may trigger anti-bot on some sites
- **SSL Verification**: Disabled globally (security consideration)
- **Single Task**: One CSV processing task per user at a time
- **Session Storage**: No persistent user data
- **Timeout**: 2-hour maximum for large datasets
- **No API Keys**: Free scraping only, no paid APIs for domain authority

---

## Use Cases

1. **Market Research**: Analyze payment infrastructure of competitors
2. **Sales Prospecting**: Identify merchants using specific payment gateways
3. **Platform Migration**: Discover current tech stack before migration
4. **Lead Generation**: Build targeted lists based on payment methods
5. **Technology Audits**: Assess e-commerce platform distribution
6. **Partnership Analysis**: Identify potential integration partners
