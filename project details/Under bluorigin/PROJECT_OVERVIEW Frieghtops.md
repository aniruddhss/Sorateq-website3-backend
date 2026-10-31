# FreightOps Platform - Project Overview

## Executive Summary
FreightOps is a comprehensive SaaS platform for freight/trucking operations management. It provides end-to-end solutions for dispatching, fleet management, HR/payroll, driver operations, and accounting for trucking companies.

## Problem Statement
Trucking companies struggle with fragmented systems for managing drivers, loads, equipment, payroll, and compliance. Coordination between dispatchers and drivers is inefficient, leading to delays and miscommunication.

## Solution
A unified platform with three integrated applications:
1. **Web Portal** - Company management dashboard for dispatchers/admins
2. **Mobile App** - Driver-facing application for load management and workflows
3. **Backend API** - Centralized REST API with JWT authentication

---

## Technical Architecture

### 1. Backend (fopssidbackend/)
**Framework**: FastAPI (Python)
**Database**: PostgreSQL (Neon.tech) with SQLite fallback for dev
**ORM**: SQLAlchemy
**Migrations**: Alembic
**Authentication**: JWT (HS256) with bcrypt password hashing
**API Version**: V1 (Clean implementation with legacy support)

#### Core Technologies:
- Python 3.8+
- FastAPI 0.104.1
- SQLAlchemy (async support with asyncpg)
- Pydantic for validation
- Uvicorn ASGI server
- APScheduler for background jobs
- Firebase Admin SDK for notifications
- Synctera API integration for banking services

#### Database Schema (88 tables total):
**V1 Core Tables**: companies, users, drivers, equipment, employees
**V1 New Tables**: driver_payment_configs, time_entries, mileage_entries, settlements
**Legacy Tables**: 80+ tables including loads, invoices, bills, maintenance records

#### Security Features:
- Rate limiting (100 req/min production, 1000 dev)
- Security headers middleware (HSTS, CSP, X-Frame-Options)
- CORS middleware (configurable origins)
- SSL/TLS with Neon.tech
- Environment-based DEBUG mode
- Connection pooling (10-30 connections)
- Password hashing with bcrypt

#### API Structure:
```
/api/v1
├── /register                    # Company registration
├── /login                       # User/admin login
├── /auth/me                     # Get current user
├── /logout                      # Logout
├── /drivers/*                   # Driver management
├── /fleet/*                     # Fleet/equipment management
├── /hr-payroll/*                # HR & payroll
├── /dispatch/*                  # Load dispatch & management
├── /dashboard/*                 # Dashboard metrics
├── /driver/equipment/*          # Driver equipment APIs
├── /driver/loads/*              # Driver load APIs
├── /driver/location             # Location tracking
├── /driver/status               # Driver status updates
├── /driver/profile              # Driver profile management
├── /driver/settlements/*        # Time/mileage tracking & payments
└── /chat/*                      # Messaging system
```

---

### 2. Web Frontend (FOPS-v0-Frontend/)
**Framework**: Next.js 16.0.0 (React 19.2.0)
**Styling**: Tailwind CSS 4.1.9
**UI Components**: Radix UI, shadcn/ui
**State Management**: SWR for data fetching
**Forms**: React Hook Form + Zod validation

#### Core Technologies:
- TypeScript 5.6.3
- Next.js App Router
- Radix UI primitives (40+ components)
- Lucide React icons
- date-fns for date manipulation
- Recharts for data visualization
- React Google Maps API
- Sonner for toast notifications

#### Application Modules:
- **Dispatch**: Load management, driver assignment, scheduling
- **Fleet**: Vehicle tracking, maintenance, compliance records
- **HR/Payroll**: Employee management, payroll processing, onboarding, documents
- **Accounting**: Invoices, bills, comprehensive accounting
- **Settings**: Company settings, user management

#### Key Features:
- Real-time chat dock (WebSocket support)
- Protected routes with AuthContext
- Responsive design (tablet/desktop optimized)
- Server-side rendering
- Automatic API documentation sync

---

### 3. Mobile App (FOPS_Mobile/)
**Framework**: Expo 54.0.0 (React Native 0.81.5)
**Navigation**: Expo Router 6.0.15
**UI**: NativeWind 4.1.23 (Tailwind for React Native)
**State Management**: Zustand 5.0.2
**Data Fetching**: TanStack React Query 5.83.0

#### Core Technologies:
- React 19.1.0
- TypeScript 5.9.3
- Expo managed workflow
- Expo Location for GPS tracking
- Expo Image Picker for camera/photos
- Lucide React Native icons
- React Native Gesture Handler

#### Application Screens:
- **Dashboard**: Load overview, stats, quick actions
- **Login/Signup**: Driver authentication
- **Join Agency**: Company join code entry
- **Pickup Process**: Multi-step pickup workflow
- **Delivery Process**: Multi-step delivery workflow
- **Load Details**: Detailed load information
- **Chat**: Messaging with dispatch
- **Settings**: Profile, equipment, notifications

#### Key Features:
- Background location tracking (60s intervals during active loads)
- Offline support with AsyncStorage caching
- Photo capture for proof of delivery/pickup
- Real-time status updates
- Network connectivity monitoring
- Workflow state persistence (resume after app restart)
- Tablet optimization (responsive grid layouts)

#### Permissions:
- Location (always + when in use)
- Camera
- Photo library access
- Media storage

---

## Core Functionalities

### 1. Authentication & User Management
- Company registration with business details (DOT/MC numbers)
- User/admin authentication (JWT)
- Driver authentication (separate from company users)
- Join code system for driver onboarding
- Role-based access control (admin, dispatcher, driver)
- Session management with token refresh

### 2. Driver Management
- Driver profiles (license, contact, emergency contact)
- Driver invitations with unique codes
- Driver status tracking (available, on_trip, off_duty, resting)
- Driver metrics and performance stats
- Equipment assignment/unassignment
- Driver documents and compliance

### 3. Fleet Management
- Equipment tracking (trucks, trailers)
- Equipment details (make, model, VIN, license plate)
- Maintenance schedules and records
- Compliance tracking
- Equipment status management
- Live location tracking
- Equipment assignment to drivers
- ELD provider integration
- Insurance and registration tracking

### 4. Dispatch & Load Management
- Load creation with full details (origin, destination, cargo)
- Load assignment to drivers/equipment
- Multi-status workflow:
  - Pending → Assigned → Dispatched → In Transit → Delivered/Cancelled
- Pickup workflow (7 stages):
  - Navigation → Arrived → Trailer Confirmed → Container Confirmed → Pickup Confirmed → Departed
- Delivery workflow (5 stages):
  - In Transit → Arrived → Docked → Unloading → Delivered
- Bill of Lading upload
- Proof of delivery with recipient signature
- Real-time load tracking
- Schedule management
- Load search and filtering
- Customer management

### 5. Driver Workflows (Mobile)
- Truck assignment confirmation
- Trailer setup verification
- Navigation to pickup/delivery
- Location check-in at sites
- Multi-step status updates
- Photo documentation
- Notes and special instructions
- Departure confirmation
- Automated status transitions

### 6. Location Tracking
- Continuous GPS tracking during active loads
- 60-second interval updates
- Location history storage
- Accuracy, altitude, speed tracking
- Background location permissions
- Low-power optimization

### 7. HR & Payroll
- Employee management (profiles, positions, departments)
- Document management (W2, I9, licenses, policies)
- Onboarding process automation
- Onboarding tasks tracking
- Payroll configuration (hourly/mileage rates)
- Payroll run creation and processing
- Payroll entries per employee
- Time tracking integration

### 8. Settlements & Payments
- Driver payment configurations (hourly vs mileage)
- Time tracking (check-in/check-out with GPS)
- Mileage tracking per load
- Automated earnings calculation
- Settlement generation (weekly/custom periods)
- Payment status tracking
- Earnings summaries and history
- Rate management per driver

### 9. Chat & Messaging
- 1-on-1 conversations (driver ↔ dispatcher)
- Team conversations
- Message history
- Unread count tracking
- Real-time message delivery
- Read status indicators
- Reply functionality
- System notifications

### 10. Dashboard & Reporting
- Company metrics overview
- Driver performance stats
- Fleet utilization
- Load statistics
- Revenue tracking
- Weight/distance summaries
- Real-time updates

### 11. Banking Integration
- Synctera API integration
- Business account creation (KYB)
- Person/entity verification
- Virtual account management
- Beneficial owner verification

### 12. Compliance & Documents
- Driver document storage
- Equipment compliance records
- Expiry date tracking
- Document categorization
- File upload/download
- Status tracking (active, expired, archived)

---

## Integration Points

### External Services:
1. **Neon.tech**: PostgreSQL database hosting with SSL
2. **Synctera**: Banking and payment processing
3. **Firebase**: Push notifications (via Firebase Admin SDK)
4. **Vercel**: Frontend hosting and deployment
5. **Railway**: Backend deployment option
6. **Expo EAS**: Mobile app building and OTA updates

### API Endpoints (60+ routes):
- V1 Auth: 4 endpoints
- V1 Drivers: 20+ endpoints
- V1 Fleet: 15+ endpoints
- V1 Dispatch: 10+ endpoints
- V1 HR/Payroll: 15+ endpoints
- V1 Driver Mobile: 25+ endpoints
- V1 Chat: 5+ endpoints
- V1 Settlements: 8+ endpoints

---

## Deployment Strategy

### Backend:
- Production: Railway or cloud hosting
- Environment variables: DATABASE_URL, SECRET_KEY, ALLOWED_ORIGINS
- Database migrations via Alembic
- Health check endpoint: `/health`
- CORS configured for web + mobile origins
- Rate limiting and security headers enabled

### Frontend:
- Vercel deployment
- Auto-deploy from git
- Environment variables: NEXT_PUBLIC_API_URL
- SSR + static optimization
- TypeScript strict mode

### Mobile:
- Expo managed workflow
- EAS Build for production APK/IPA
- OTA updates via Expo Updates
- Environment: development, preview, production profiles
- Bundle identifier: app.rork.driver.trucking

---

## Development Setup

### Backend:
```bash
cd fopssidbackend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
# Configure .env file
python run.py
```

### Frontend:
```bash
cd FOPS-v0-Frontend
pnpm install
pnpm dev
```

### Mobile:
```bash
cd FOPS_Mobile
pnpm install
pnpm start  # Development
pnpm android  # Run on Android
pnpm ios  # Run on iOS
```

---

## Project Status

### Completed:
- ✅ V1 authentication system (company + driver)
- ✅ Driver management and onboarding
- ✅ Fleet/equipment management
- ✅ Load dispatch and assignment
- ✅ Driver mobile workflows (pickup/delivery)
- ✅ Location tracking
- ✅ Chat messaging system
- ✅ HR/Payroll with onboarding
- ✅ Settlements (time + mileage tracking)
- ✅ Dashboard metrics
- ✅ Database migrations (88 tables)
- ✅ Production-ready backend (security, rate limiting)

### Known Issues:
- ⚠️ Next.js Turbopack panic error (fixed with config updates)
- ⚠️ TypeScript version needs update to 5.6.3
- ⚠️ CORS origins need production domain configuration
- ⚠️ Android emulator requires 10.0.2.2 for localhost API

### Future Enhancements:
- Hours of Service (HOS) tracking
- Advanced analytics and reporting
- Multi-language support
- Dark mode (partial implementation)
- Tablet-specific UI optimizations
- Offline mode improvements
- WebSocket real-time updates for chat

---

## Key Metrics

- **Total Lines of Code**: ~50,000+
- **Backend API Routes**: 60+
- **Database Tables**: 88
- **Mobile App Screens**: 15+
- **Web Portal Modules**: 5 major modules
- **Supported Platforms**: iOS, Android, Web
- **Authentication Method**: JWT (8-hour expiry)
- **Location Update Interval**: 60 seconds
- **Rate Limit**: 100 requests/minute (production)

---

## Technology Stack Summary

**Backend**: FastAPI + SQLAlchemy + PostgreSQL + JWT + Alembic  
**Web**: Next.js 16 + React 19 + TypeScript + Tailwind + Radix UI  
**Mobile**: Expo + React Native + TypeScript + NativeWind + Zustand  
**Database**: PostgreSQL (Neon.tech) with 88 tables  
**Deployment**: Vercel (web) + Railway (backend) + EAS (mobile)  
**APIs**: RESTful with JWT authentication  
**Real-time**: WebSocket support for chat  
**Location**: Expo Location with background tracking  
**Storage**: AsyncStorage (mobile), SWR cache (web)
