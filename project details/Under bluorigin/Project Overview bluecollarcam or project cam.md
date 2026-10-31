# BlueCollarCam - Project Overview

## Problem Statement
Construction teams lack efficient tools to document, manage, and collaborate on projects in real-time. Traditional methods involve disconnected tools for photos, tasks, accounting, and communication, leading to inefficiency and poor project visibility.

## Solution
BlueCollarCam (Project Cam Plus) - A comprehensive construction project management platform with mobile and web applications, providing unified project documentation, team collaboration, task management, financial tracking, and real-time communication.

---

## Architecture

### Platform Structure
- **Backend**: Supabase (PostgreSQL + Auth + Storage + Realtime)
- **Mobile**: React Native (Expo) - iOS/Android
- **Web**: Next.js 16 with TypeScript
- **Database**: PostgreSQL with Row Level Security (RLS)
- **Storage**: Supabase Storage (photos, files, avatars, logos)

### Technology Stack

#### Backend
- **Supabase**: PostgreSQL, authentication, storage, real-time subscriptions
- **Express.js**: Additional API endpoints (optional)
- **TypeScript**: Type-safe development
- **Node.js 18+**: Runtime environment
- **Libraries**: `@supabase/supabase-js`, `express`, `cors`, `helmet`, `morgan`, `winston`

#### Mobile (React Native/Expo)
- **React Native 0.81.5**: Cross-platform mobile framework
- **Expo ~54.0**: Development platform and toolchain
- **TypeScript**: Type safety
- **Navigation**: `@react-navigation/native`, `@react-navigation/bottom-tabs`, `@react-navigation/stack`
- **State Management**: React Context API (`AuthContext`)
- **Storage**: `@react-native-async-storage/async-storage`
- **Camera**: `expo-camera`, `expo-image-picker`, `expo-image-manipulator`
- **Location**: `expo-location` (GPS tracking)
- **UI**: Custom design system with themed components
- **Supabase Client**: `@supabase/supabase-js` 2.45.4

#### Web (Next.js)
- **Next.js 16.0.10**: React framework with SSR
- **React 19.2.0**: UI library
- **TypeScript**: Type safety
- **UI Components**: Radix UI (40+ components), Shadcn/ui patterns
- **Styling**: TailwindCSS 4.1.9 with custom configuration
- **Forms**: `react-hook-form` with `zod` validation
- **Charts**: `recharts` for data visualization
- **State Management**: React Context (`AuthContext`)
- **Theme**: `next-themes` for dark/light mode
- **Icons**: `lucide-react`

---

## Database Schema (22 Tables)

### Core Tables
1. **profiles** - User accounts, push tokens, language preferences
2. **business_info** - Business details for invoicing, logos
3. **teams** - Team/organization management
4. **team_members** - Memberships with roles (owner, project_manager, member, viewer)
5. **team_invitations** - Email invitations with status tracking
6. **team_groups** - Sub-groups for access control
7. **team_group_members** - Group membership assignments
8. **projects** - Construction projects with GPS, budget, status
9. **project_favorites** - User bookmarks
10. **project_group_assignments** - Group access to projects
11. **project_photos** - Photos with GPS, JSONB tags, audio annotations
12. **project_tasks** - Tasks with urgency, status, assignments
13. **project_timeline** - Unified activity feed
14. **project_comments** - Comments with reply support
15. **project_notes** - Public/private notes
16. **project_files** - Document attachments (PDF, etc.)
17. **project_accounting_entries** - Income/expense tracking
18. **invoices** - Invoice management with status tracking
19. **conversations** - Team/project chat threads
20. **messages** - Chat messages
21. **message_reads** - Read receipts
22. **notifications** - Push notifications

### Database Features
- **13 Migration Files**: Sequential schema deployment
- **Row Level Security (RLS)**: Enabled on all 22 tables
- **Triggers**: Auto-update timestamps, budget calculations, task numbering, notifications
- **Indexes**: Optimized for performance (email, team, project, date, location)
- **PostGIS Support**: GPS-based project searches
- **JSONB**: Flexible metadata storage for tags

---

## Security Model

### Authentication
- JWT-based authentication via Supabase Auth
- Email/password registration with verification
- Session persistence with auto-refresh tokens
- Password reset functionality
- Social providers support (Google, Apple - optional)

### Authorization
- **Row Level Security (RLS)** on all tables
- Team-based access control
- Role hierarchy: Owner → Project Manager → Member → Viewer
- Private notes visible only to creator
- Storage bucket policies for file access
- Team membership validation for all operations

### Access Control Hierarchy
```
Team Owner
  ├── Full access to team and all projects
  └── Manage members and settings

Project Manager
  ├── Manage projects
  ├── Create/update tasks
  └── Manage project members

Member
  ├── Upload photos
  ├── Create tasks
  └── Comment on items

Viewer
  └── Read-only access
```

---

## Core Features & Functionalities

### 1. Authentication & User Management
- User registration with email/password
- Sign in/sign out with session management
- Profile management (name, company, phone, avatar)
- Business information setup (for invoicing)
- Language preference (English/Spanish)
- Push notification token registration

### 2. Team Management
- Create and manage teams
- Invite members via email
- Assign roles (Owner, PM, Member, Viewer)
- Sub-groups for access control
- Team avatar and settings
- Pending invitation tracking

### 3. Project Management
- Create projects with full details (name, address, type, budget, dates)
- Project types: Construction, Renovation, Maintenance, Inspection
- Status tracking: Active, Completed, On Hold, Archived
- GPS location for projects
- Cover photo and description
- Project favorites/bookmarks
- Search and filter (by name, address, status, location)
- Sort options (Latest, Last Updated, Nearby, Favorites, Active)
- Budget tracking with progress visualization
- Project statistics (team size, photos, files, notes count)
- Assign groups to projects for access control

### 4. Photo Management
- Upload photos with GPS location
- Thumbnail generation (via Edge Function)
- Comments on photos
- JSONB tags with colors
- Audio annotations
- Photo gallery with grid view
- Filter and search photos
- Display metadata (uploader, date, location)

### 5. Task Management
- Create tasks with assignments
- Urgency levels: Non-urgent, Medium, Urgent
- Status: Pending, In Progress, Completed
- Auto-generated task numbers (#001, #002, etc.)
- Due dates
- Task descriptions
- Link tasks to notes
- Notification on assignment and completion

### 6. Financial Tracking
- Income and expense entries
- Category management
- Budget vs. spent calculations
- Automatic project budget updates
- Date-based tracking
- Budget summaries with remaining amount
- Transaction history

### 7. Notes System
- Public notes (visible to team)
- Private notes (creator only)
- Rich text content
- Link to tasks
- Timestamps and author tracking

### 8. File Management
- Upload documents (PDF, Word, etc.)
- File size and type tracking
- Storage in Supabase buckets
- Download functionality

### 9. Timeline & Activity Feed
- Unified activity stream
- Event types: photo, comment, task, invoice, status_change, member_added
- Chronological display
- Flexible JSONB data for different event types

### 10. Communication
- Team conversations
- Project-specific chats
- Direct messages
- Read receipts
- Message history
- Real-time messaging support

### 11. Notifications
- Push notifications (iOS, Android, Web)
- Types: photo, comment, task_completed, task_assigned, project_shared, team_invitation, message
- Read/unread status
- Project and task references
- Expo push notification integration

### 12. Invoice Management
- Create invoices for projects
- Invoice numbering system
- Status: Pending, Paid, Overdue, Cancelled
- Due date tracking
- Payment date recording
- Invoice notes

---

## Custom Database Functions (RPC)

### Implemented Functions
1. **get_project_budget_summary(project_id)** - Calculate income/expenses/remaining
2. **get_project_stats(project_id)** - Project statistics (team, photos, files, notes count)
3. **search_projects(query)** - Full-text search with relevance ranking
4. **get_nearby_projects(lat, lng, radius_km)** - GPS-based project search (PostGIS)
5. **get_user_projects(user_id)** - List user's accessible projects with team validation
6. **mark_all_notifications_read(user_id)** - Bulk notification update
7. **get_unread_message_count(user_id)** - Unread messages counter
8. **generate_task_number(project_id)** - Auto-generate sequential task numbers

---

## Edge Functions (Deno)

### 1. send-push-notification
- Send Expo push notifications to iOS/Android devices
- Triggered by database events or manual calls
- Handles notification formatting and delivery

### 2. generate-thumbnail
- Automatic image thumbnail generation
- Optimizes photo storage
- Triggered on photo upload

---

## Storage Buckets

### 1. project-photos
- **Access**: Private
- **Size Limit**: 10MB
- **MIME Types**: image/jpeg, image/png, image/heic
- **Policy**: Team members can upload/view

### 2. project-files
- **Access**: Private
- **Size Limit**: 50MB
- **MIME Types**: PDF, Word documents, etc.
- **Policy**: Team members can upload/view

### 3. avatars
- **Access**: Public
- **Size Limit**: 2MB
- **MIME Types**: image/jpeg, image/png
- **Policy**: Users can upload own avatar

### 4. business-logos
- **Access**: Public
- **Size Limit**: 2MB
- **MIME Types**: image/jpeg, image/png, image/svg+xml
- **Policy**: Users can upload own logo

---

## Mobile App (React Native)

### Navigation Structure
**Bottom Tab Navigation (5 Tabs)**:
1. **Home** - Project dashboard with search, filters, team members
2. **Inbox** - Team conversations and messages
3. **Camera** - Photo capture (elevated center button)
4. **Teams** - Team management, members, groups
5. **Settings** - Profile, business info, preferences, logout

### Screens Implemented

#### Authentication
- `SignInScreen` - Email/password login
- `SignUpScreen` - User registration

#### Main Screens
- `HomeScreen` - Project dashboard with API integration
- `InboxScreen` - Messaging (placeholder)
- `CameraScreen` - Photo capture with GPS
- `TeamsScreen` - Team management
- `SettingsScreen` - User settings and preferences
- `EditProfileScreen` - Profile editing with avatar upload

#### Project Screens
- `ProjectDetailScreen` - Project overview with tabs
- `TimelineTab` - Activity feed
- `PhotosTab` - Photo gallery and upload
- `TasksTab` - Task list and creation
- `AccountingTab` - Budget and transactions
- `NotesTab` - Notes management
- `FilesTab` - Document management
- `PhotoEditorScreen` - Photo editing and annotation

### Mobile Features
- Real API integration with Supabase
- Pull-to-refresh on all lists
- Loading states and error handling
- Empty states for no data
- Favorite toggling with persistence
- Image picker and camera integration
- GPS location capture
- Form validation
- Optimistic UI updates

### Design System
- **Color Palette**: Primary Blue (#3B82F6), Orange Accent (#F97316), Status colors (Green, Red, Yellow)
- **Typography**: 11px-32px, weights 400-700
- **Spacing**: 4px grid system (4, 8, 12, 16, 20, 24, 32, 40, 48)
- **Borders**: Radius 8-20px, 3-level shadow system
- **iOS Optimization**: 44pt touch targets, safe area handling

---

## Web Application (Next.js)

### Page Structure
- `/` - Landing/Login page
- `/signup` - Registration page
- `/dashboard` - Main dashboard (protected)
- `/dashboard/projects` - Project list
- `/dashboard/projects/[id]` - Project detail with tabs
- `/dashboard/team` - Team management
- `/dashboard/settings` - User settings (profile, business info)
- `/dashboard/inbox` - Messaging (placeholder)

### Features Implemented
- Server-side rendering (SSR)
- Protected routes with authentication
- Responsive design (mobile, tablet, desktop)
- Dark/light theme support
- Form validation with react-hook-form + zod
- Real-time data loading
- Search and filter functionality
- Modal dialogs for actions
- Toast notifications
- Data visualization with charts
- File upload with drag-and-drop

### UI Components (40+ Radix UI Components)
- Accordion, Alert Dialog, Avatar, Button, Card
- Checkbox, Dialog, Dropdown Menu, Form, Input
- Label, Popover, Progress, Radio Group, Select
- Separator, Slider, Switch, Tabs, Toast, Tooltip
- And more...

---

## Service Layer Architecture

### Shared Services (Mobile & Web)
Both platforms implement identical service modules:

1. **authService** - Sign up, sign in, sign out, session management, password reset
2. **profileService** - Get/update profile, avatar upload, business info CRUD
3. **teamService** - Team CRUD, members, invitations, groups
4. **projectService** - Project CRUD, favorites, search, filtering
5. **photoService** - Upload, metadata, filtering, GPS tagging
6. **taskService** - Task CRUD, assignments, completion tracking
7. **noteService** - Note CRUD, public/private, task linking
8. **accountingService** - Entry CRUD, budget summaries

### Additional Services
- **groupService** (Mobile) - Team group management
- **conversationService** (Planned) - Messaging functionality

---

## Data Flow

### Mobile App
```
User Action → Screen Component → Service Layer → Supabase Client → API
                                                                      ↓
User Interface ← Context (State) ← Response Handler ← API Response ←
```

### Web App
```
User Action → Page/Component → Service Layer → Supabase Client → API
                                                                   ↓
UI Update ← Context (State) ← Response Handler ← API Response ←
```

### Real-time Features
```
Database Event → Supabase Realtime → WebSocket → Client Subscription → UI Update
```

---

## API Integration

### REST API (Supabase Auto-generated)
- `GET /rest/v1/{table}` - List records with filters
- `POST /rest/v1/{table}` - Create record
- `PATCH /rest/v1/{table}?id=eq.{id}` - Update record
- `DELETE /rest/v1/{table}?id=eq.{id}` - Delete record
- `POST /rest/v1/rpc/{function}` - Call custom function

### Storage API
- `POST /storage/v1/object/{bucket}/{path}` - Upload file
- `GET /storage/v1/object/public/{bucket}/{path}` - Download file
- `DELETE /storage/v1/object/{bucket}/{path}` - Delete file

### Query Features
- Filtering: `?status=eq.active`, `?budget=gt.10000`
- Ordering: `?order=created_at.desc`
- Pagination: `?limit=10&offset=0`
- Relations: `?select=*,profiles(*),team_members(count)`
- Full-text search: `?name=fts.construction`

---

## Deployment Architecture

### Backend
- **Supabase Cloud**: Managed PostgreSQL, Auth, Storage, Realtime
- **Database**: Automatic backups, point-in-time recovery
- **Edge Functions**: Deno runtime on Supabase infrastructure
- **CDN**: Global distribution for storage

### Mobile
- **iOS**: App Store deployment via Expo/EAS Build
- **Android**: Google Play Store deployment
- **OTA Updates**: Expo Updates for JS bundle updates
- **Push Notifications**: Expo Push Notification service

### Web
- **Vercel/Netlify**: Static site with SSR
- **CDN**: Global edge network
- **Environment Variables**: Secure credential management
- **Analytics**: Vercel Analytics integrated

---

## Development Workflow

### Setup Process
1. Create Supabase project
2. Run 13 database migrations in order
3. Create storage buckets with policies
4. Configure environment variables
5. Install dependencies
6. Run development servers

### Environment Variables

#### Backend
```
SUPABASE_URL=https://project.supabase.co
SUPABASE_ANON_KEY=anon-key
SUPABASE_SERVICE_ROLE_KEY=service-role-key
DATABASE_URL=postgresql://...
```

#### Mobile
```
EXPO_PUBLIC_SUPABASE_URL=https://project.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=anon-key
```

#### Web
```
NEXT_PUBLIC_SUPABASE_URL=https://project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=anon-key
```

---

## Key Documentation Files

### Backend
- `BACKEND_API_SPECIFICATION.md` - Complete API documentation
- `README.md` - Setup and deployment guide
- `IMPLEMENTATION_SUMMARY.md` - Implementation details
- `DEPLOYMENT_CHECKLIST.md` - Production deployment steps
- `QUICK_START.md` - Quick setup guide

### Mobile
- `README.md` - Mobile app overview
- `USER_GUIDE.md` - Feature documentation (1207 lines)
- `API_INTEGRATION.md` - API setup guide
- `IMPLEMENTATION_COMPLETE.md` - Implementation summary
- `PHOTO_EDITOR_IMPLEMENTATION.md` - Photo feature details
- `NAVIGATION_FLOW.md` - Navigation structure
- `QUICK_START.md` - Quick setup guide
- `RUNNING_ON_IPHONE.md` - iOS deployment

### Web
- `QUICK_START.md` - Web app setup
- `IMPLEMENTATION_COMPLETE.md` - Implementation details

---

## Project Statistics

### Codebase
- **Backend**: 13 migration files, Express server, Supabase config
- **Mobile**: 20+ screens, 9 services, custom design system, 40+ components
- **Web**: 15+ pages, 8 services, 40+ UI components, responsive layouts
- **Total Tables**: 22 database tables with full RLS
- **API Methods**: 50+ service methods per platform
- **Lines of Documentation**: 5000+ lines across all docs

### Features
- **User Management**: Registration, authentication, profiles, business info
- **Team Collaboration**: Teams, members, roles, invitations, groups
- **Project Tracking**: Projects, favorites, GPS, budgets, status
- **Photo System**: Upload, GPS tags, comments, audio, thumbnails
- **Task Management**: Creation, assignment, urgency, completion
- **Financial**: Accounting entries, budgets, invoices
- **Communication**: Messaging, notifications, timeline
- **File Storage**: Photos, documents, avatars, logos

---

## Success Metrics

### Technical Achievements
- Full-stack implementation with mobile + web parity
- Type-safe TypeScript across all platforms
- Comprehensive Row Level Security implementation
- Real-time capabilities with WebSocket support
- Optimized database with indexes and triggers
- Modular service architecture for maintainability
- Consistent API patterns across platforms

### Business Value
- Single platform for all construction project needs
- Real-time team collaboration
- GPS-based project tracking
- Complete financial oversight
- Mobile-first documentation workflow
- Cross-platform accessibility (iOS, Android, Web)
- Scalable multi-tenant architecture

---

## Future Enhancements (Potential)

- Real-time messaging implementation
- Video upload and playback
- Offline mode with sync
- Advanced analytics dashboard
- Automated reporting and exports
- Integration with third-party tools (QuickBooks, etc.)
- Mobile widgets for quick photo capture
- Apple Watch companion app
- Advanced photo editing tools
- AR/VR project visualization
