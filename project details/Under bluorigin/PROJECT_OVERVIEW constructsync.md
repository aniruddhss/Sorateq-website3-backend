# ConstructSync - Complete Project Overview

**Version:** 1.0.0  
**Last Updated:** December 27, 2025  
**Status:** Production Ready

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Solution](#solution)
4. [Use Cases & Target Users](#use-cases--target-users)
5. [System Architecture](#system-architecture)
6. [Technology Stack](#technology-stack)
7. [Core Features & Functionalities](#core-features--functionalities)
8. [Database Architecture](#database-architecture)
9. [Security & Authentication](#security--authentication)
10. [Mobile Features](#mobile-features)
11. [Web Dashboard Features](#web-dashboard-features)
12. [API Structure](#api-structure)
13. [Deployment Architecture](#deployment-architecture)

---

## Executive Summary

**ConstructSync** is a comprehensive, full-stack construction management platform designed to streamline operations for construction companies, project managers, site supervisors, and field workers. The platform consists of three interconnected applications:

- **Backend API** (Node.js/Express/PostgreSQL)
- **Web Dashboard** (Next.js/React)
- **Mobile App** (React Native/Expo)

The system enables real-time collaboration, job tracking, safety management, worker check-ins with geofencing, budget monitoring, and advanced analytics for construction projects.

---

## Problem Statement

Construction companies face numerous challenges in managing their operations:

### 1. **Communication Breakdown**
- Disconnected teams across multiple job sites
- Lack of real-time information sharing between office and field workers
- Paper-based job diaries and safety reports prone to loss
- Delayed incident reporting and hazard identification

### 2. **Time & Attendance Issues**
- Manual timekeeping leading to payroll errors
- Workers unable to verify their on-site hours
- No validation of worker location during check-in
- Buddy punching and time theft

### 3. **Project Management Complexity**
- Difficulty tracking multiple jobs, sites, and teams simultaneously
- No centralized view of job status and progress
- Poor budget visibility and cost overruns
- Subcontractor coordination challenges

### 4. **Safety Compliance**
- Inconsistent safety reporting
- Lack of hazard tracking and near-miss documentation
- Missing safety inspection records
- No central repository for safety training certificates

### 5. **Resource Management**
- Inefficient team allocation across projects
- Poor visibility into worker availability
- Difficulty in tracking materials and equipment
- No analytics on labor efficiency

### 6. **Data Fragmentation**
- Multiple spreadsheets and disconnected systems
- No single source of truth for project data
- Difficulty generating reports and insights
- Compliance documentation scattered across platforms

---

## Solution

ConstructSync provides an integrated, cloud-based construction management ecosystem that solves these challenges through:

### Unified Platform
- **Single Database**: All data stored in centralized PostgreSQL database
- **Multi-Platform Access**: Web dashboard for managers, mobile apps for field workers
- **Real-Time Sync**: Instant updates across all devices and users
- **Offline Capability**: Mobile app works offline, syncs when connected

### Smart Geofencing
- GPS-based site boundaries (50m-1000m radius)
- Workers can only check in when physically on-site
- Automatic location verification
- Worker location tracking for safety and compliance

### Role-Based Access
- **Super Admin**: Full system control, multi-company management
- **Company Admin**: Company-wide settings and user management
- **Project Manager**: Job creation, budget oversight, team management
- **Site Supervisor**: Day-to-day operations, worker oversight
- **Foreman**: Task assignment, team coordination
- **Worker**: Job check-in, task completion, safety reporting
- **Subcontractor**: Limited access to assigned jobs
- **Viewer**: Read-only access for stakeholders

### Comprehensive Features
- Job & site management with Google Maps integration
- Team & worker management with hourly rates
- Time tracking with billable hours calculation
- Safety incident & hazard reporting
- Budget tracking with line-item breakdown
- Subcontractor contracts & payments
- Real-time weather data for job sites
- Document management & storage
- Advanced analytics & reporting

---

## Use Cases & Target Users

### Primary Use Cases

#### 1. Construction Company Management
**Users:** Company Admins, Project Managers

**Scenarios:**
- Monitor all active job sites from a centralized dashboard
- Allocate teams and resources across multiple projects
- Track budget vs. actual costs in real-time
- Generate reports for stakeholders and clients
- Manage subcontractor contracts and payments
- Review safety incidents and compliance metrics

#### 2. Field Operations Management
**Users:** Site Supervisors, Foremen

**Scenarios:**
- Create and assign daily tasks to workers
- Track job progress and milestone completion
- Record job diary entries with weather conditions
- Conduct safety inspections on-site
- Upload photos and documents from the field
- Coordinate with office staff in real-time

#### 3. Worker Time & Attendance
**Users:** Field Workers

**Scenarios:**
- Check in/out of job sites using mobile device
- View assigned tasks and mark them complete
- Report safety hazards immediately
- Track personal earnings and hours worked
- Upload progress photos and notes
- Receive job notifications and updates

#### 4. Safety & Compliance
**Users:** All Roles

**Scenarios:**
- Report safety incidents with photo evidence
- Document near-miss events to prevent accidents
- Track hazards until resolution
- Maintain safety training records
- Conduct routine safety inspections
- Generate compliance reports for audits

#### 5. Budget & Financial Tracking
**Users:** Project Managers, Company Admins

**Scenarios:**
- Create job budgets with category breakdown
- Track expenses against allocated amounts
- Monitor labor costs via check-in logs
- Manage subcontractor invoices and payments
- Analyze job profitability and margins
- Generate financial forecasts

#### 6. Subcontractor Coordination
**Users:** Project Managers, Subcontractors

**Scenarios:**
- Create contracts with scope and payment terms
- Track subcontractor progress and deliverables
- Process milestone payments
- Share job documents and specifications
- Monitor subcontractor compliance
- Evaluate subcontractor performance

### Target Industries
- **Residential Construction**: Home builders, renovators
- **Commercial Construction**: Office buildings, retail spaces
- **Civil Engineering**: Roads, bridges, infrastructure
- **Specialty Trades**: Electrical, plumbing, HVAC contractors
- **Property Development**: Multi-site project coordination

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                            │
├──────────────────────────┬──────────────────────────────────┤
│   Web Dashboard          │     Mobile Application           │
│   (Next.js 16)           │     (React Native/Expo)          │
│   - Desktop/Tablet UI    │     - iOS & Android              │
│   - Admin & Managers     │     - Workers & Field Staff      │
└──────────────────────────┴──────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      API LAYER                               │
│   REST API (Express.js + TypeScript)                         │
│   - JWT Authentication & Authorization                       │
│   - Rate Limiting & Security (Helmet, CORS)                  │
│   - Swagger API Documentation                                │
│   - Request Validation (Zod)                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   SERVICE LAYER                              │
│   Business Logic Modules:                                    │
│   - Authentication & User Management                         │
│   - Jobs, Sites, Tasks, Teams                                │
│   - Safety, Budgets, Check-ins                               │
│   - Subcontractors, Weather, Analytics                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  REPOSITORY LAYER                            │
│   Data Access Objects (DAOs):                                │
│   - Database abstraction                                     │
│   - Query optimization                                       │
│   - Soft delete support                                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  DATABASE LAYER                              │
│   PostgreSQL 14+                                             │
│   - 40+ Tables with relationships                            │
│   - Stored procedures & triggers                             │
│   - Comprehensive indexing                                   │
│   - Audit logging & soft deletes                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               EXTERNAL SERVICES                              │
│   - Google Maps API (Geolocation)                            │
│   - WeatherAPI.com (Weather data)                            │
│   - Storage Services (Document uploads)                      │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow Example: Worker Check-In

```
Mobile App → POST /api/check-ins
    ↓
JWT Validation Middleware
    ↓
Request Validation (Zod)
    ↓
Check-ins Controller
    ↓
Check-ins Service
    ├─ Verify job exists
    ├─ Validate worker access
    ├─ Check geofence (lat/long within radius)
    ├─ Ensure no active check-in
    └─ Calculate billable rate
    ↓
Check-ins Repository
    ↓
PostgreSQL Database
    ├─ Insert check_in_logs record
    ├─ Update worker_locations
    └─ Return check-in record
    ↓
Response to Mobile App (with check-in details)
```

---

## Technology Stack

### Backend (construct-sync-backend)

#### Core Framework
- **Node.js** (v20+): JavaScript runtime
- **Express.js** (v4.18): Web application framework
- **TypeScript** (v5.3): Type-safe JavaScript

#### Database
- **PostgreSQL** (v14+): Primary relational database
- **pg** (v8.11): PostgreSQL client for Node.js
- Connection pooling and transaction management

#### Authentication & Security
- **jsonwebtoken** (v9.0): JWT token generation and validation
- **bcryptjs** (v2.4): Password hashing
- **helmet** (v7.1): HTTP header security
- **cors** (v2.8): Cross-Origin Resource Sharing
- **express-rate-limit** (v7.1): API rate limiting

#### Validation & Documentation
- **zod** (v3.22): Schema validation
- **swagger-jsdoc** (v6.2): API documentation generation
- **swagger-ui-express** (v5.0): Swagger UI hosting

#### Development & Testing
- **tsx** (v4.7): TypeScript execution
- **jest** (v29.7): Testing framework
- **supertest** (v6.3): HTTP assertion testing
- **ts-jest** (v29.4): TypeScript testing support

#### Utilities
- **dotenv** (v16.3): Environment variable management
- **uuid** (v9.0): UUID generation

### Frontend - Web (Construct-Sync-Web)

#### Core Framework
- **Next.js** (v16.0): React framework with SSR/SSG
- **React** (v18): UI library
- **TypeScript** (v5.3): Type safety

#### State Management & Data Fetching
- **@tanstack/react-query** (v5.90): Server state management
- Async state management
- Automatic caching and refetching
- Optimistic updates

#### UI Components & Styling
- **Radix UI**: Headless component library
  - Dialog, Dropdown, Select, Tabs, Toast, etc.
  - Accessibility built-in (ARIA compliant)
- **Tailwind CSS** (v3.4): Utility-first CSS
- **tailwindcss-animate**: Animation utilities
- **lucide-react** (v0.454): Icon library
- **next-themes**: Dark/light mode support

#### Forms & Validation
- **react-hook-form** (v7.60): Form state management
- **@hookform/resolvers** (v3.10): Form validation
- **zod** (v3.25): Schema validation

#### Maps & Location
- **@react-google-maps/api** (v2.20): Google Maps integration
- Custom components for site mapping
- Geofencing visualization

#### Charts & Data Visualization
- **recharts** (v2.15): Chart library
- Line, bar, pie charts for analytics

#### Utilities
- **date-fns** (v4.1): Date manipulation
- **clsx** + **tailwind-merge**: CSS class management
- **sonner** (v1.7): Toast notifications

#### Testing
- **@playwright/test** (v1.57): End-to-end testing
- Comprehensive test suites for all features

### Mobile (rork-construct-sync)

#### Core Framework
- **React Native** (v0.81): Native mobile framework
- **Expo** (v54.0): Development platform
- **Expo Router** (v6.0): File-based routing
- **React** (v19.1): UI library

#### Navigation & UI
- **@react-navigation/native** (v7.1): Navigation library
- **react-native-screens** (v4.16): Native screen components
- **react-native-gesture-handler** (v2.28): Touch gestures
- **react-native-reanimated** (v4.1): Animations
- **react-native-safe-area-context** (v5.6): Safe area handling

#### Expo Modules
- **expo-location** (v19.0): GPS and geolocation
- **expo-image-picker** (v17.0): Camera and gallery access
- **expo-document-picker** (v14.0): File selection
- **expo-image** (v3.0): Optimized image component
- **expo-constants** (v18.0): App constants
- **expo-blur** (v15.0): Blur effects
- **expo-haptics** (v15.0): Haptic feedback
- **expo-linear-gradient** (v15.0): Gradients
- **expo-status-bar** (v3.0): Status bar control

#### State & Data
- **@tanstack/react-query** (v5.83): Server state
- **zustand** (v5.0): Client state management
- **@react-native-async-storage/async-storage** (v2.2): Persistent storage

#### Maps & Location
- **react-native-maps** (v1.20): Native map component
- Geofencing support
- Custom markers and overlays

#### Styling
- **nativewind** (v4.0): Tailwind CSS for React Native
- Consistent styling with web app

#### Icons & Assets
- **lucide-react-native** (v0.475): Icon library
- **@expo/vector-icons** (v15.0): Icon sets

#### Development
- **TypeScript** (v5.9): Type safety
- **Babel** (v7.25): JavaScript transpiler
- **ESLint** (v9.31): Code linting

---

## Core Features & Functionalities

### 1. Authentication & User Management

#### Features
- **Secure Registration & Login**
  - Email/password authentication
  - JWT token-based sessions
  - Refresh token mechanism
  - Password reset via email token

- **Role-Based Access Control (RBAC)**
  - 8 distinct user roles with granular permissions
  - Company-level data isolation
  - Cross-company access prevention

- **User Profile Management**
  - Personal information updates
  - Hourly rate configuration for workers
  - Avatar/profile photo support
  - Activity tracking and audit logs

#### API Endpoints
```
POST   /api/auth/signup           - Register new user
POST   /api/auth/login            - Authenticate user
POST   /api/auth/forgot-password  - Request password reset
POST   /api/auth/reset-password   - Reset password with token
POST   /api/auth/refresh          - Refresh access token
GET    /api/auth/me               - Get current user profile
```

---

### 2. Sites Management

#### Features
- **Site Creation & Management**
  - Google Maps integration for location selection
  - Address autocomplete with Places API
  - Configurable geofence radius (50m-1000m)
  - Visual circular boundary on map

- **Site Details**
  - Basic information (name, address, status)
  - GPS coordinates (latitude/longitude)
  - Site status tracking (planning, active, on hold, completed, archived)
  - Site-specific budgets and expenses
  - Site media uploads (photos, videos, documents)

- **Site Organization**
  - Multiple sites per company
  - Site zones for large projects
  - Job association with sites
  - Team assignments

#### Status Flow
```
Planning → Active → (On Hold) → Completed → Archived
```

#### API Endpoints
```
GET    /api/sites                - List all sites
POST   /api/sites                - Create new site
GET    /api/sites/:id            - Get site details
PATCH  /api/sites/:id            - Update site
DELETE /api/sites/:id            - Soft delete site
GET    /api/sites/:id/jobs       - Get jobs for site
```

---

### 3. Jobs Management

#### Features
- **Job Creation & Tracking**
  - Job number generation
  - Job type categorization
  - Start and end date scheduling
  - Priority levels (low, medium, high, urgent, critical)
  - Status tracking (draft, planned, in_progress, on_hold, completed, cancelled, archived)

- **Job Organization**
  - Site association
  - Job blocks (building sections)
  - Job units (apartments, floors)
  - Hierarchical structure: Job → Blocks → Units

- **Job Details**
  - Description and requirements
  - Client information
  - Budget allocation
  - Team and worker assignments
  - Manager assignments
  - Subcontractor contracts

- **Job Documentation**
  - Document uploads (contracts, permits, blueprints)
  - Photo gallery with timestamps
  - Job diary entries with weather
  - Progress milestones

- **Job Variations**
  - Change orders and variations
  - Variation number tracking
  - Amount and description
  - Status workflow (draft, submitted, approved, rejected, completed)

#### Status Flow
```
Draft → Planned → In Progress → (On Hold) → Completed/Cancelled → Archived
```

#### API Endpoints
```
GET    /api/jobs                     - List all jobs
POST   /api/jobs                     - Create new job
GET    /api/jobs/:id                 - Get job details
PATCH  /api/jobs/:id                 - Update job
DELETE /api/jobs/:id                 - Soft delete job
POST   /api/jobs/:id/blocks          - Add job block
POST   /api/jobs/:id/units           - Add job unit
GET    /api/jobs/:id/documents       - Get job documents
POST   /api/jobs/:id/photos          - Upload job photo
GET    /api/jobs/:id/diary           - Get job diary entries
POST   /api/jobs/:id/diary           - Add diary entry
GET    /api/jobs/:id/variations      - Get variations
POST   /api/jobs/:id/variations      - Create variation
GET    /api/jobs/:id/workers         - Get assigned workers
POST   /api/jobs/:id/workers         - Assign worker to job
```

---

### 4. Tasks Management

#### Features
- **Task Creation & Assignment**
  - Create tasks for jobs or job units
  - Assign to specific workers
  - Priority levels
  - Due date tracking

- **Task Organization**
  - Job-level tasks
  - Unit-specific tasks
  - Task dependencies (future feature)

- **Task Tracking**
  - Status updates (pending, in_progress, completed, cancelled, blocked)
  - Progress notes
  - Time tracking integration

#### Status Flow
```
Pending → In Progress → Completed/Cancelled/Blocked
```

#### API Endpoints
```
GET    /api/tasks                 - List all tasks
POST   /api/tasks                 - Create task
GET    /api/tasks/:id             - Get task details
PATCH  /api/tasks/:id             - Update task
DELETE /api/tasks/:id             - Soft delete task
GET    /api/tasks/assigned        - Get tasks assigned to current user
```

---

### 5. Teams Management

#### Features
- **Team Creation**
  - Team name and description
  - Company-level teams

- **Team Member Management**
  - Add/remove team members
  - Assign roles (lead, member, viewer)
  - View team composition

- **Team Assignments**
  - Assign teams to jobs
  - Team-level permissions

#### API Endpoints
```
GET    /api/teams                 - List all teams
POST   /api/teams                 - Create team
GET    /api/teams/:id             - Get team details
PATCH  /api/teams/:id             - Update team
DELETE /api/teams/:id             - Soft delete team
POST   /api/teams/:id/members     - Add team member
DELETE /api/teams/:id/members/:userId - Remove member
```

---

### 6. Worker Check-Ins & Time Tracking

#### Features
- **Geofenced Check-In**
  - GPS-based location verification
  - Check-in only when within site radius
  - Automatic location recording

- **Time Tracking**
  - Check-in and check-out timestamps
  - Automatic duration calculation
  - Hourly rate from user profile
  - Billable amount calculation (hours × rate)

- **Check-In Validation**
  - Prevent multiple active check-ins
  - Require job association
  - Verify worker assignment to job

- **Worker Earnings**
  - View personal check-in history
  - Total hours worked
  - Total earnings calculated

#### Calculation Logic
```
duration_hours = (check_out_time - check_in_time) / 3600
billable_amount = duration_hours × hourly_rate
```

#### API Endpoints
```
POST   /api/check-ins              - Check in to job
POST   /api/check-ins/:id/checkout - Check out
GET    /api/check-ins              - Get check-in logs
GET    /api/check-ins/active       - Get active check-in
GET    /api/mobile/check-ins/my-earnings - Get worker earnings
```

---

### 7. Safety Management

#### Features
- **Safety Incidents**
  - Incident date and time
  - Description and severity (minor, moderate, major, critical, fatal)
  - Status tracking (open, investigating, resolved, closed)
  - Photo evidence upload
  - Reporter and witness information

- **Hazard Reports**
  - Hazard type classification (slip/trip/fall, electrical, chemical, fire, etc.)
  - Severity assessment
  - Resolution tracking
  - Site/job association

- **Near-Miss Reports**
  - Proactive incident prevention
  - Potential severity rating
  - Corrective action tracking

- **Safety Inspections**
  - Scheduled and routine inspections
  - Inspection types (routine, safety, quality, compliance, final, pre-start)
  - Findings documentation
  - Pass/fail status
  - Inspector tracking

- **Safety Training Records**
  - Training type and certification
  - Training date and expiry
  - Certificate document upload
  - Compliance tracking

#### Status Flow (Incidents/Hazards)
```
Open → Investigating → Resolved → Closed
```

#### API Endpoints
```
GET    /api/safety/incidents           - List incidents
POST   /api/safety/incidents           - Report incident
GET    /api/safety/incidents/:id       - Get incident details
PATCH  /api/safety/incidents/:id       - Update incident
GET    /api/safety/hazards             - List hazards
POST   /api/safety/hazards             - Report hazard
GET    /api/safety/near-miss           - List near-miss reports
POST   /api/safety/near-miss           - Report near-miss
GET    /api/safety/inspections         - List inspections
POST   /api/safety/inspections         - Create inspection
GET    /api/safety/training            - Get training records
POST   /api/safety/training            - Add training record
```

---

### 8. Budget Management

#### Features
- **Job-Level Budgets**
  - Total budget allocation
  - Budget line items by category
  - Allocated vs. spent tracking
  - Budget variance calculation

- **Budget Categories**
  - Labor
  - Materials
  - Equipment
  - Subcontractors
  - Permits & Fees
  - Custom categories

- **Cost Tracking**
  - Transaction recording (expense, purchase, payment, refund, adjustment)
  - Category-level expense tracking
  - Real-time spend monitoring

- **Budget Analytics**
  - Budget utilization percentage
  - Variance analysis
  - Cost projections
  - Profitability metrics

#### Budget Calculation
```
allocated_budget = SUM(budget_line_items.allocated_amount)
spent_budget = SUM(budget_line_items.spent_amount)
variance = allocated_budget - spent_budget
utilization = (spent_budget / allocated_budget) × 100
```

#### API Endpoints
```
GET    /api/budgets                      - List all budgets
POST   /api/budgets                      - Create budget
GET    /api/budgets/:id                  - Get budget details
PATCH  /api/budgets/:id                  - Update budget
DELETE /api/budgets/:id                  - Soft delete budget
POST   /api/budgets/:id/line-items       - Add line item
PATCH  /api/budgets/:id/line-items/:lineId - Update line item
DELETE /api/budgets/:id/line-items/:lineId - Delete line item
GET    /api/budgets/:id/transactions     - Get transactions
POST   /api/budgets/:id/transactions     - Add transaction
```

---

### 9. Subcontractor Management

#### Features
- **Subcontractor Profiles**
  - Business name and ABN
  - Contact information (email, phone, address)
  - Trade specialization
  - Active/inactive status
  - Rating and performance tracking

- **Subcontractor Contracts**
  - Contract number generation
  - Contract title and description
  - Contract value and payment terms
  - Start, end, and completion dates
  - Progress tracking (percentage complete)
  - Status workflow (draft, active, completed, terminated, expired)
  - Job association

- **Contract Payments**
  - Payment amount and date
  - Payment method (cash, check, bank transfer, credit card, EFT, other)
  - Reference number
  - Payment notes

#### Status Flow
```
Draft → Active → Completed/Terminated/Expired
```

#### API Endpoints
```
GET    /api/subcontractors                       - List subcontractors
POST   /api/subcontractors                       - Create subcontractor
GET    /api/subcontractors/:id                   - Get details
PATCH  /api/subcontractors/:id                   - Update subcontractor
DELETE /api/subcontractors/:id                   - Soft delete
GET    /api/subcontractors/:id/contracts         - Get contracts
POST   /api/subcontractors/:id/contracts         - Create contract
GET    /api/subcontractors/contracts/:contractId - Get contract
PATCH  /api/subcontractors/contracts/:contractId - Update contract
POST   /api/subcontractors/contracts/:contractId/payments - Add payment
```

---

### 10. Weather Integration

#### Features
- **Real-Time Weather Data**
  - Current temperature, humidity, wind speed
  - Visibility and precipitation
  - Weather conditions (sunny, cloudy, rainy, etc.)

- **Weather Forecasts**
  - 5-14 day forecasts
  - Hourly conditions
  - Precipitation probability

- **Risk Assessment**
  - Automatic risk level calculation
  - **High Risk**: Wind > 40 km/h OR precipitation > 10mm OR visibility < 2km
  - **Medium Risk**: Wind > 25 km/h OR precipitation > 5mm OR visibility < 5km
  - **Low Risk**: All other conditions

- **Job-Specific Weather**
  - Weather for job site coordinates
  - Workable days prediction
  - Risk days identification

#### Integration
- **Provider**: WeatherAPI.com
- **Data Points**: Temperature, precipitation, wind, visibility, humidity, UV index

#### API Endpoints
```
GET /api/mobile/weather/job/:jobId?days=5      - Get weather for job
GET /api/mobile/weather/current?lat=X&lon=Y    - Get current weather
GET /api/mobile/weather/forecast?lat=X&lon=Y&days=5 - Get forecast
```

---

### 11. Analytics & Reporting

#### Features
- **Site Overview**
  - Active sites count
  - Total jobs
  - Labor hours tracked
  - Budget summaries

- **Job Profitability**
  - Revenue vs. costs
  - Profit margins
  - Job-level financial performance
  - Variation impact analysis

- **Labor Efficiency**
  - Hours worked per job
  - Cost per hour
  - Worker productivity metrics
  - Overtime tracking

- **Business Health**
  - Cash flow analysis
  - Outstanding payments
  - Budget utilization
  - Project completion rates

- **Custom Reports**
  - Date range filtering
  - Export capabilities
  - Printable formats

#### API Endpoints
```
GET /api/analytics/overview          - Business overview
GET /api/analytics/labor             - Labor analytics
GET /api/analytics/profitability     - Profitability metrics
```

---

### 12. Mobile-Specific Features

#### Worker Home Screen
- Active check-in status
- Today's assigned tasks
- Quick check-in/check-out
- Recent notifications

#### Job Details (Mobile)
- Job information
- Check-in to job (with geofence validation)
- View tasks
- Upload photos
- Report safety issues
- View other workers on site

#### Worker Earnings
- Total hours worked
- Total earnings
- Check-in history
- Hourly rate display

#### Offline Support
- Cache recent data
- Queue actions for sync
- Automatic sync when online

#### Push Notifications
- Task assignments
- Job updates
- Safety alerts
- Check-in reminders

---

### 13. Settings & Configuration

#### Company Settings
- Company profile
- Default settings
- Notification preferences
- Integration settings

#### User Settings
- Profile information
- Password change
- Email preferences
- Mobile app settings

#### System Settings (Admin Only)
- System-wide configurations
- Feature toggles
- Rate limits
- Maintenance mode

---

## Database Architecture

### Overview
- **Database**: PostgreSQL 14+
- **Total Tables**: 40+
- **Total Indexes**: 100+
- **Total ENUMs**: 20+

### Key Design Principles
1. **Soft Deletes**: All primary tables include `deleted_at` timestamp for logical deletion
2. **Audit Trail**: `created_at` and `updated_at` timestamps on all records
3. **Comprehensive Indexing**: Optimized for query performance
4. **Referential Integrity**: Foreign key constraints with cascading deletes
5. **Type Safety**: Extensive use of ENUM types for status fields
6. **UUID Primary Keys**: Distributed system friendly

### Core Entity Relationships

```
companies
    ├── users (1:N)
    ├── sites (1:N)
    ├── jobs (1:N)
    ├── teams (1:N)
    ├── subcontractors (1:N)
    └── materials (1:N)

sites
    ├── jobs (1:N)
    ├── site_media (1:N)
    ├── site_budgets (1:1)
    ├── site_zones (1:N)
    ├── safety_incidents (1:N)
    └── safety_inspections (1:N)

jobs
    ├── job_blocks (1:N)
    │   └── job_units (1:N)
    │       └── job_tasks (1:N)
    ├── job_tasks (1:N)
    ├── job_budgets (1:1)
    │   └── budget_line_items (1:N)
    ├── job_workers (N:M)
    ├── job_managers (N:M)
    ├── job_documents (1:N)
    ├── job_photos (1:N)
    ├── job_diary_entries (1:N)
    ├── job_variations (1:N)
    ├── check_in_logs (1:N)
    ├── safety_incidents (1:N)
    └── subcontractor_contracts (1:N)

users
    ├── check_in_logs (1:N)
    ├── job_tasks (assigned_to) (1:N)
    ├── team_members (N:M)
    ├── safety_incidents (reported_by) (1:N)
    ├── worker_locations (1:N)
    └── safety_training_records (1:N)

subcontractors
    ├── subcontractor_contracts (1:N)
    │   └── contract_payments (1:N)

teams
    └── team_members (N:M)
        └── users
```

### Critical ENUM Types

```sql
user_role: super_admin, company_admin, project_manager, site_supervisor, 
           foreman, worker, subcontractor, viewer

job_status: draft, planned, in_progress, on_hold, completed, cancelled, archived

task_status: pending, in_progress, completed, cancelled, blocked

site_status: planning, active, on_hold, completed, archived

safety_status: open, investigating, resolved, closed

priority_level: low, medium, high, urgent, critical

severity_level: minor, moderate, major, critical, fatal

contract_status: draft, active, completed, terminated, expired

notification_type: task_assigned, task_completed, task_overdue, job_updated, 
                   material_requested, material_low_stock, safety_incident, 
                   inspection_due, payment_received, document_uploaded, 
                   mention, system
```

### Performance Optimizations

#### Indexes
- **Foreign Keys**: All foreign keys indexed
- **Status Fields**: Indexed for filtering (job_status, task_status, etc.)
- **Timestamps**: Indexed for date range queries
- **Compound Indexes**: For common query patterns (user_id + job_id)
- **Partial Indexes**: For active records (WHERE deleted_at IS NULL)

#### Queries
- **Soft Delete Filtering**: All queries include `WHERE deleted_at IS NULL`
- **Connection Pooling**: Reusable database connections
- **Prepared Statements**: SQL injection prevention and performance
- **Transaction Support**: ACID compliance for critical operations

---

## Security & Authentication

### Authentication Strategy

#### JWT (JSON Web Tokens)
- **Access Token**: Short-lived (1 hour)
- **Refresh Token**: Long-lived (7 days)
- **Secure Storage**: 
  - Web: HTTP-only cookies (future) or localStorage
  - Mobile: Expo SecureStore (encrypted device storage)

#### Token Structure
```json
{
  "userId": "uuid",
  "email": "user@example.com",
  "role": "project_manager",
  "companyId": "uuid",
  "iat": 1703000000,
  "exp": 1703003600
}
```

### Authorization Levels

#### Role Hierarchy
```
Super Admin (Level 8)
    └── Company Admin (Level 7)
        ├── Project Manager (Level 6)
        │   ├── Site Supervisor (Level 5)
        │   │   └── Foreman (Level 4)
        │   │       └── Worker (Level 3)
        │   └── Subcontractor (Level 2)
        └── Viewer (Level 1)
```

#### Permission Matrix

| Resource | Super Admin | Company Admin | PM | Supervisor | Foreman | Worker | Viewer |
|----------|-------------|---------------|-----|-----------|---------|--------|--------|
| Companies | CRUD | R | - | - | - | - | - |
| Sites | CRUD | CRUD | CRUD | R | R | R | R |
| Jobs | CRUD | CRUD | CRUD | RU | RU | R | R |
| Tasks | CRUD | CRUD | CRUD | CRUD | CRUD | RU | R |
| Workers | CRUD | CRUD | CRUD | R | R | R | - |
| Budgets | CRUD | CRUD | CRUD | R | R | - | R |
| Safety | CRUD | CRUD | CRUD | CRUD | CRUD | CR | R |
| Check-ins | CRUD | R | R | R | R | CRU (own) | R |

**Legend:** C=Create, R=Read, U=Update, D=Delete

### Security Measures

#### API Security
- **Helmet.js**: HTTP header security
  - Content Security Policy
  - X-Frame-Options
  - X-Content-Type-Options
  - Strict-Transport-Security

- **CORS**: Cross-Origin Resource Sharing
  - Whitelist allowed origins
  - Credentials support

- **Rate Limiting**: 
  - 100 requests per 15 minutes per IP
  - Prevents brute force and DDoS

#### Data Security
- **Password Hashing**: bcrypt (10 salt rounds)
- **SQL Injection Prevention**: Parameterized queries
- **XSS Prevention**: Input sanitization
- **CSRF Protection**: Token validation (future)

#### Data Isolation
- **Company-Level**: All queries filtered by `company_id`
- **User-Level**: Workers can only see assigned jobs
- **Soft Deletes**: Deleted records remain for audit but are inaccessible

#### Logging & Auditing
- **Audit Logs Table**: Tracks all critical actions
  - User ID and action
  - Entity type and ID
  - Old and new values (JSON)
  - IP address and timestamp

---

## API Structure

### Base URL
- **Development**: `http://localhost:5000/api`
- **Production**: `https://your-domain.com/api`

### Request/Response Format

#### Standard Success Response
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Operation successful"
}
```

#### Standard Error Response
```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {
    // Additional error information
  }
}
```

### HTTP Status Codes
- `200 OK`: Successful GET, PATCH, DELETE
- `201 Created`: Successful POST
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate resource
- `500 Internal Server Error`: Server error

### API Modules

#### Authentication
```
POST   /api/auth/signup
POST   /api/auth/login
POST   /api/auth/forgot-password
POST   /api/auth/reset-password
POST   /api/auth/refresh
GET    /api/auth/me
```

#### Sites
```
GET    /api/sites
POST   /api/sites
GET    /api/sites/:id
PATCH  /api/sites/:id
DELETE /api/sites/:id
```

#### Jobs
```
GET    /api/jobs
POST   /api/jobs
GET    /api/jobs/:id
PATCH  /api/jobs/:id
DELETE /api/jobs/:id
POST   /api/jobs/:id/blocks
POST   /api/jobs/:id/units
```

#### Tasks
```
GET    /api/tasks
POST   /api/tasks
GET    /api/tasks/:id
PATCH  /api/tasks/:id
DELETE /api/tasks/:id
```

#### Teams
```
GET    /api/teams
POST   /api/teams
GET    /api/teams/:id
PATCH  /api/teams/:id
DELETE /api/teams/:id
POST   /api/teams/:id/members
```

#### Workers
```
GET    /api/workers
POST   /api/workers
GET    /api/workers/:id
PATCH  /api/workers/:id
DELETE /api/workers/:id
```

#### Check-ins
```
POST   /api/check-ins
POST   /api/check-ins/:id/checkout
GET    /api/check-ins
GET    /api/check-ins/active
```

#### Safety
```
GET    /api/safety/incidents
POST   /api/safety/incidents
GET    /api/safety/hazards
POST   /api/safety/hazards
GET    /api/safety/near-miss
POST   /api/safety/near-miss
```

#### Budgets
```
GET    /api/budgets
POST   /api/budgets
GET    /api/budgets/:id
PATCH  /api/budgets/:id
POST   /api/budgets/:id/line-items
```

#### Subcontractors
```
GET    /api/subcontractors
POST   /api/subcontractors
GET    /api/subcontractors/:id
PATCH  /api/subcontractors/:id
POST   /api/subcontractors/:id/contracts
```

#### Mobile
```
GET    /api/mobile/jobs/my-jobs
GET    /api/mobile/tasks/my-tasks
GET    /api/mobile/check-ins/my-earnings
GET    /api/mobile/weather/job/:jobId
```

### API Documentation
- **Swagger UI**: Available at `/api-docs`
- **Interactive Testing**: Try endpoints directly from browser
- **Schema Definitions**: Request/response models
- **Authentication**: Test with JWT tokens

---

## Deployment Architecture

### Hosting Recommendations

#### Backend
- **Railway**: Recommended for easy deployment
- **Heroku**: Alternative option
- **AWS EC2**: For custom setups
- **DigitalOcean**: Cost-effective option

#### Database
- **Railway PostgreSQL**: Managed database
- **AWS RDS**: Production-grade PostgreSQL
- **Supabase**: PostgreSQL with additional features

#### Web Frontend
- **Vercel**: Optimized for Next.js
- **Netlify**: Alternative deployment
- **AWS Amplify**: Full-stack hosting

#### Mobile App
- **Expo EAS**: Build and deploy iOS/Android
- **App Store**: iOS distribution
- **Google Play**: Android distribution

### Environment Variables

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/database
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=constructsync
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password

# JWT
JWT_SECRET=your_jwt_secret_key
JWT_EXPIRES_IN=1h
REFRESH_TOKEN_EXPIRES_IN=7d

# Server
PORT=5000
NODE_ENV=production

# External APIs
WEATHER_API_KEY=your_weatherapi_key
GOOGLE_MAPS_API_KEY=your_google_maps_key

# CORS
ALLOWED_ORIGINS=https://your-web-app.com,https://mobile-app-domain
```

#### Web Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=https://your-backend-api.com/api
NEXT_PUBLIC_GOOGLE_MAPS_KEY=your_google_maps_key
```

#### Mobile App (.env)
```bash
EXPO_PUBLIC_API_URL=https://your-backend-api.com/api
EXPO_PUBLIC_GOOGLE_MAPS_KEY=your_google_maps_key
```

### Deployment Checklist

#### Pre-Deployment
- [ ] All environment variables configured
- [ ] Database migrations executed
- [ ] Production database backed up
- [ ] SSL certificates configured
- [ ] CORS origins whitelisted
- [ ] API keys secured
- [ ] Error monitoring setup (Sentry, LogRocket)
- [ ] Performance monitoring (New Relic, DataDog)

#### Backend Deployment
1. Build TypeScript: `npm run build`
2. Set environment variables
3. Run migrations: `npm run migrate`
4. Start server: `npm start`
5. Verify health check: `GET /health`

#### Web Deployment
1. Build production: `npm run build`
2. Test build locally: `npm run start`
3. Deploy to Vercel/Netlify
4. Verify deployment

#### Mobile Deployment
1. Update app version in `app.config.js`
2. Build for iOS: `eas build --platform ios --profile production`
3. Build for Android: `eas build --platform android --profile production`
4. Submit to App Store / Google Play

### Monitoring & Maintenance

#### Health Checks
- Backend: `GET /health` endpoint
- Database: Connection pool monitoring
- API Response times
- Error rates

#### Logging
- Application logs (Winston, Pino)
- Database query logs
- Audit logs
- Error tracking (Sentry)

#### Backups
- **Database**: Daily automated backups
- **Media Files**: S3 or cloud storage with versioning
- **Retention**: 30 days minimum

---

## Future Enhancements

### Planned Features
1. **Real-Time Chat**: Team communication within the app
2. **Video Calls**: On-site collaboration with office
3. **AI-Powered Analytics**: Predictive insights and recommendations
4. **Materials Management**: Inventory tracking and ordering
5. **Equipment Tracking**: Asset management and maintenance
6. **Invoice Generation**: Automated billing from check-ins
7. **Client Portal**: External access for stakeholders
8. **Integration APIs**: Connect with accounting software (Xero, QuickBooks)
9. **Advanced Reporting**: Custom report builder
10. **Biometric Authentication**: Face ID / Touch ID for mobile

### Scalability Considerations
- **Microservices**: Break monolith into services
- **Message Queue**: RabbitMQ or AWS SQS for async tasks
- **Caching**: Redis for frequently accessed data
- **CDN**: CloudFront or Cloudflare for static assets
- **Load Balancing**: Multiple backend instances
- **Database Replication**: Read replicas for scaling

---

## Development Team Guidelines

### Getting Started

#### Prerequisites
- Node.js 20+
- PostgreSQL 14+
- pnpm or npm
- Git

#### Backend Setup
```bash
cd construct-sync-backend
npm install
cp .env.example .env
# Configure .env with database credentials
npm run migrate
npm run dev
```

#### Web Setup
```bash
cd Construct-Sync-Web
npm install
cp .env.example .env.local
# Configure .env.local with API URL
npm run dev
```

#### Mobile Setup
```bash
cd rork-construct-sync
npm install
cp .env.example .env
# Configure .env with API URL
npm run start
```

### Code Standards

#### TypeScript
- Strict type checking enabled
- Interfaces for all data structures
- No `any` types without justification

#### API Development
- RESTful conventions
- Zod validation for all inputs
- Swagger documentation for all endpoints

#### Testing
- Unit tests for services
- Integration tests for APIs
- E2E tests for critical flows
- Target: 80%+ code coverage

#### Git Workflow
- Feature branches: `feature/feature-name`
- Bug fixes: `bugfix/bug-name`
- Pull requests required
- Code review before merge

---

## Support & Documentation

### Documentation Resources
- **API Docs**: `/api-docs` (Swagger UI)
- **README Files**: Each project has comprehensive README
- **Implementation Guides**: Detailed guides in project root
- **Testing Guides**: QA testing procedures documented

### Contact & Support
- **Technical Issues**: Raise GitHub issues
- **Feature Requests**: Create feature request issues
- **Security Concerns**: Email security@constructsync.com

---

## License & Legal

### Software License
- Proprietary software
- All rights reserved
- Commercial use requires license

### Third-Party Licenses
- Open source dependencies: See package.json
- Google Maps API: Subject to Google's terms
- WeatherAPI: Subject to WeatherAPI terms

---

## Conclusion

ConstructSync is a production-ready, full-featured construction management platform that addresses the complex needs of modern construction companies. With its comprehensive feature set, robust security, and scalability, it provides a solid foundation for managing construction operations efficiently.

The platform's three-tier architecture (backend API, web dashboard, mobile app) ensures flexibility and accessibility for all stakeholders, from company executives to field workers.

**Key Strengths:**
- ✅ Complete CRUD operations for all entities
- ✅ Advanced geofencing and GPS tracking
- ✅ Real-time weather intelligence
- ✅ Comprehensive safety management
- ✅ Flexible budget tracking
- ✅ Mobile-first worker experience
- ✅ Rich analytics and reporting
- ✅ Production-ready codebase

**Next Steps:**
1. Deploy to production environment
2. Onboard beta testing users
3. Gather user feedback
4. Implement planned enhancements
5. Scale infrastructure as needed

---

**Document Version:** 1.0  
**Last Updated:** December 27, 2025  
**Prepared By:** Development Team  
**Status:** Complete & Production Ready
