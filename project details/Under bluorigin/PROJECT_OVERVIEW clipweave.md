# ClipWeave - Project Overview

## Problem Statement
Event organizers (weddings, birthdays, conferences) struggle to:
- Collect videos from multiple guests efficiently
- Manually edit and merge scattered video clips
- Create professional highlight reels that require video editing expertise
- Share final compilations with attendees

## Solution
ClipWeave is an AI-powered video compilation platform that automates the entire workflow from collection to creation:
- **Capture**: QR code/link-based video submission system
- **Weave**: AI-driven automatic video sequencing, editing, and stylization
- **Share**: Professional highlight reels ready for download and distribution

## Architecture

### Backend (`clipweave/`)
- **Framework**: Express.js with TypeScript
- **Server**: Node.js, deployed on Railway (Nixpacks)
- **Database**: SQLite (development), Drizzle ORM for type-safety
- **API Documentation**: Swagger/OpenAPI integration

### Frontend (`v0-clip-weave-frontend/`)
- **Framework**: Next.js 15 with React 19
- **Styling**: Tailwind CSS with Radix UI components
- **State Management**: React Context (Auth)
- **Deployment**: Vercel

## Core Technologies

### Video Processing
- **FFmpeg**: Local video editing (trim, merge, transitions, filters, effects, text overlay, audio manipulation, speed adjustment, rotation, cropping, resizing)
- **fluent-ffmpeg**: Node.js FFmpeg wrapper
- **Shotstack API**: Cloud video rendering and composition

### AI & Analysis
- **Twelve Labs Pegasus 1.2**: Video understanding (visual/audio analysis, scene detection, semantic search, embeddings)
- **OpenAI GPT-4**: Creative editing decisions (transition selection, pacing, color grading, text placement)

### Storage & Infrastructure
- **Cloudflare R2**: S3-compatible object storage with zero egress fees
- **AWS SDK**: S3 operations (upload, download, signed URLs)
- **BullMQ + Redis**: Background job queue for video processing
- **IORedis**: Redis client for queue management

### Security & Middleware
- **JWT (jsonwebtoken)**: Stateless authentication
- **bcryptjs**: Password hashing
- **Helmet**: Security headers
- **CORS**: Cross-origin configuration
- **express-rate-limit**: DDoS protection
- **Morgan**: HTTP request logging
- **Compression**: Response optimization

## Database Schema

### Tables
1. **users**: Account management (userId, email, name, plan, password)
2. **events**: Event containers (eventId, title, description, date, uploadCode, coverImage)
3. **clips**: Video submissions (clipId, originalUrl, normalizedUrl, r2Key, duration, resolution, status, uploaderInfo)
4. **clipAnalysis**: AI metadata (scenes, keyframes, tags, actions, people, audioEmotion, qualityScore, embeddings, rawTwelvelabs)
5. **compositions**: Shotstack renders (compositionId, clipIds, sequenceJson, status, outputUrl)
6. **processingJobs**: Job tracking (jobId, type, inputJson, outputJson, status)
7. **mergedOutputs**: FFmpeg results (outputId, clipIds, sequence, transitionType, r2Key, status)

## Key Features

### 1. Authentication & Authorization
- User registration/login with JWT
- Protected routes with Bearer token middleware
- Profile management

### 2. Event Management
- Create events with unique upload codes
- Generate QR codes for guest sharing
- Event dashboard with analytics
- Multi-event support per user

### 3. Video Upload & Storage
- Direct file upload (multipart/form-data)
- URL-based upload (fetch and store)
- Automatic R2 storage integration
- Video metadata extraction (duration, resolution, codec)
- Upload code-based public submission

### 4. Video Editing (FFmpeg)
**Basic Operations**:
- Trim: Extract portions (startTime, duration)
- Merge: Combine multiple clips with transitions (fade, dissolve, wipe)
- Resize: Resolution conversion (4K/1080p/720p/480p)
- Rotate: Orientation correction (90/180/270 degrees)
- Crop: Aspect ratio adjustment
- Reverse: Playback reversal

**Effects & Filters**:
- Visual filters (grayscale, sepia, vignette, negative, blur, sharpen)
- Brightness, contrast, saturation adjustment
- Speed control (0.1x - 4.0x)

**Audio Manipulation**:
- Extract audio (mp3/aac/wav)
- Replace/add audio tracks
- Volume control
- Fade in/out

**Text & Overlays**:
- Dynamic text placement (top/center/bottom)
- Custom font (Roboto-Regular.ttf)
- Background with opacity
- Timing control (startTime, duration)

**Pipeline System**:
- Chain multiple operations atomically
- Single API call for complex workflows
- Efficient processing (no intermediate uploads)

### 5. AI Weave (Intelligent Video Generation)
**Workflow**:
1. User selects clips and ordering
2. System creates Twelve Labs index
3. Each clip analyzed separately (visual/audio understanding)
4. Analysis sent to OpenAI GPT-4
5. AI generates optimal FFmpeg pipeline
6. Automatic execution and R2 upload
7. Returns preview/download URLs

**AI Decision Making**:
- Transition selection based on mood/content
- Color grading for cohesive aesthetic
- Text overlay placement with smart timing
- Speed adjustments for dramatic effect
- Scene pacing and flow optimization
- Highlight identification

**API Endpoints**:
- `/api/aiweave/execute`: Full workflow (analyze + generate)
- `/api/aiweave/preview`: Pipeline preview without execution
- `/api/aiweave/execute-pipeline`: Execute custom/modified pipeline

### 6. Video Analysis (Twelve Labs)
**Index Management**:
- Create semantic search indexes
- List all indexes
- Organize videos by events

**Content Indexing**:
- Upload videos for AI processing
- Task status monitoring
- Video metadata extraction

**Analysis Types**:
- Summary: Video content description
- Chapter: Automatic chapter generation with timestamps
- Highlight: Key moment identification
- Topic: Main topic extraction

**Search Capabilities**:
- Semantic search ("find scenes with dancing")
- Visual and audio search options
- Confidence scoring
- Timestamp-based results

**Embeddings**:
- Text-to-vector conversion
- Video-to-vector conversion
- Similarity matching

### 7. Cloud Video Editing (Shotstack)
- Composition creation with clip sequences
- Render status tracking
- Output format configuration (mp4/gif/jpg)
- Resolution selection (1080p/720p/SD/mobile)
- Transition support (fade/wipe/zoom)
- Style presets (default/montage/minimal)
- Audio track integration

### 8. Storage Management (Cloudflare R2)
- Direct file upload with multipart support
- URL-based video fetching and storage
- Organized key structure (events/{eventId}/videos, processed, merged)
- Signed URL generation for secure access
- Upload signed URLs for frontend direct upload
- Configurable expiration (default: 1 hour)
- Custom domain support for public URLs
- Video metadata retrieval
- Deletion with cleanup

### 9. Background Processing
- BullMQ queue system with Redis
- Job retry logic (3 attempts, exponential backoff)
- Long-running task management
- Status tracking and monitoring

## Frontend Features

### Pages
- **Landing**: Hero section, features showcase, pricing
- **Signup/Login**: Authentication forms with validation
- **Dashboard**: Event creation, QR code generation, event grid
- **Upload**: Public video submission via upload code
- **Event Detail**: Multi-tab interface (Uploads, Storyboard, Brand Kit, Export)

### Components
- **Event Tabs**:
  - Uploads: View all submitted clips, metadata display
  - Storyboard: Drag-and-drop clip ordering, AI Weave generation, progress tracking
  - Brand Kit: Customization options
  - Export: Download and sharing options
- **QR Code Display**: Dynamic QR generation with upload links
- **Protected Routes**: Authentication wrapper for private pages
- **AI Search Modal**: Semantic video search interface
- **Theme Provider**: Dark/light mode support

### State Management
- Auth Context: User session, token management, auto-logout on 401
- Local Storage: Token persistence, user data caching

### API Integration
- Axios instance with interceptors
- Automatic token injection
- Error handling with redirects
- Response data normalization

## API Structure

### Authentication Routes
- `POST /api/auth/register`: Create account
- `POST /api/auth/login`: User login
- `GET /api/auth/me`: Get profile
- `PUT /api/auth/me`: Update profile
- `POST /api/auth/logout`: Logout

### Event Routes
- `POST /api/events`: Create event
- `GET /api/events/user/me`: List user's events
- `GET /api/events/:eventId`: Event details
- `GET /api/events/code/:uploadCode`: Public event lookup
- `PUT /api/events/:eventId`: Update event
- `DELETE /api/events/:eventId`: Delete event
- `GET /api/events/:eventId/share`: Get share info with QR

### Clip Routes
- `POST /api/clips`: Submit clip (public with upload code)
- `GET /api/clips/event/:eventId`: List event clips
- `GET /api/clips/:clipId`: Clip details
- `DELETE /api/clips/:clipId`: Remove clip
- `GET /api/clips/:clipId/analysis`: Get AI analysis

### FFmpeg Routes
- `POST /api/ffmpeg/trim`: Trim video
- `POST /api/ffmpeg/merge`: Merge clips
- `POST /api/ffmpeg/transition`: Add transitions
- `POST /api/ffmpeg/speed`: Adjust playback speed
- `POST /api/ffmpeg/filter`: Apply visual filters
- `POST /api/ffmpeg/rotate`: Rotate video
- `POST /api/ffmpeg/crop`: Crop dimensions
- `POST /api/ffmpeg/resize`: Change resolution
- `POST /api/ffmpeg/text`: Add text overlay
- `POST /api/ffmpeg/audio/add`: Add/replace audio
- `POST /api/ffmpeg/audio/extract`: Extract audio
- `POST /api/ffmpeg/reverse`: Reverse playback
- `GET /api/ffmpeg/metadata`: Get video details
- `POST /api/ffmpeg/pipeline`: Chain operations
- `GET /api/ffmpeg/outputs/:eventId`: List outputs
- `GET /api/ffmpeg/outputs/single/:outputId`: Output details
- `DELETE /api/ffmpeg/outputs/:outputId`: Delete output

### AI Weave Routes
- `POST /api/aiweave/execute`: Full AI workflow
- `POST /api/aiweave/preview`: Pipeline preview
- `POST /api/aiweave/execute-pipeline`: Execute pipeline

### Twelve Labs Routes
- `POST /api/twelvelabs/indexes`: Create index
- `GET /api/twelvelabs/indexes`: List indexes
- `POST /api/twelvelabs/clips/:clipId/index`: Index clip
- `GET /api/twelvelabs/tasks/:taskId/status`: Check status
- `POST /api/twelvelabs/clips/:clipId/analyze`: Analyze video
- `GET /api/twelvelabs/clips/:clipId/analysis`: Get analysis
- `POST /api/twelvelabs/search`: Semantic search
- `POST /api/twelvelabs/embeddings/text`: Text embeddings
- `POST /api/twelvelabs/embeddings/video`: Video embeddings
- `GET /api/twelvelabs/videos/:indexId`: List videos
- `GET /api/twelvelabs/videos/:indexId/:videoId`: Video details

### Cloudflare Routes
- `POST /api/cloudflare/upload`: Upload file
- `POST /api/cloudflare/upload-url`: Upload from URL
- `GET /api/cloudflare/signed-url/:key`: Get signed URL
- `POST /api/cloudflare/upload-signed-url`: Get upload URL
- `DELETE /api/cloudflare/videos/:key`: Delete video
- `GET /api/cloudflare/metadata/:key`: Get metadata

### Shotstack Routes
- `POST /api/shotstack/compositions`: Create composition
- `POST /api/shotstack/render/:compositionId`: Render
- `GET /api/shotstack/status/:renderId`: Check status
- `GET /api/shotstack/compositions`: List compositions
- `GET /api/shotstack/compositions/:compositionId`: Composition details

### Health Routes
- `GET /health`: Basic health check
- `GET /api/health`: API health status
- `GET /api/health/detailed`: System information

## Development Workflow

### Setup
1. Clone repository
2. Install dependencies: `npm install` (backend), `pnpm install` (frontend)
3. Configure environment variables (`.env`)
4. Initialize database: `npm run db:seed`
5. Start backend: `npm run dev` (port 5000)
6. Start frontend: `npm run dev` (port 3000)

### Testing
- Backend: Jest with Supertest
- Test suites: Authentication, Clips, Events, FFmpeg, Twelve Labs, Cloudflare, Shotstack
- Run: `npm test` or `npm run test:watch`
- Coverage: `npm run test:coverage`

### Database Management
- Generate migrations: `npm run db:generate`
- Push schema: `npm run db:push`
- Run migrations: `npm run db:migrate`
- Seed data: `npm run db:seed`
- Visual browser: `npm run db:studio`

### Deployment
- Backend: Railway with Nixpacks
- Frontend: Vercel with automatic Git integration
- Database: SQLite (dev), PostgreSQL option for production
- Worker: Separate Railway service for BullMQ

## Environment Variables

### Required
- `JWT_SECRET`: JWT signing key
- `TWELVE_LABS_API_KEY`: Video analysis API key
- `OPENAI_API_KEY`: AI decision-making API key
- `CLOUDFLARE_R2_ACCESS_KEY_ID`: R2 storage access
- `CLOUDFLARE_R2_SECRET_ACCESS_KEY`: R2 storage secret
- `CLOUDFLARE_R2_BUCKET_NAME`: Bucket name
- `CLOUDFLARE_R2_ENDPOINT`: R2 endpoint URL
- `CLOUDFLARE_ACCOUNT_ID`: Cloudflare account ID

### Optional
- `SHOTSTACK_API_KEY`: Cloud rendering (stage/production)
- `SHOTSTACK_ENV`: Environment (stage/v1)
- `REDIS_HOST`: Queue management
- `REDIS_PORT`: Queue management
- `REDIS_PASSWORD`: Queue management
- `CLOUDFLARE_R2_PUBLIC_URL`: Custom domain
- `CORS_ORIGIN`: Frontend URL
- `PORT`: Server port (default: 5000)
- `NODE_ENV`: Environment (development/production)
- `DATABASE_PATH`: SQLite file path

## User Flows

### Event Creation Flow
1. User registers/logs in
2. Creates event with title, date, description
3. Receives unique upload code and QR code
4. Shares QR/link with guests

### Guest Upload Flow
1. Guest scans QR or visits link
2. Enters upload code
3. Selects video from device
4. Video uploads to R2
5. Confirmation and redirect

### AI Weave Flow
1. User views event clips in dashboard
2. Opens Storyboard tab
3. Drags clips to reorder
4. Enters reel title
5. Clicks "Generate with AI"
6. System progress: Indexing → Analyzing → Generating → Processing
7. Final video appears with preview, download, copy link
8. Can view pipeline details (transitions, filters, effects)

### Manual Editing Flow
1. Select clips in Storyboard
2. Click "Preview Pipeline"
3. Review AI-generated structure
4. Modify operations (change transitions, adjust filters, edit text)
5. Execute modified pipeline
6. Download final video

## Performance Optimizations
- Response compression middleware
- Rate limiting per IP
- Temporary file cleanup after processing
- Background job processing for long tasks
- Signed URLs with expiration
- Cloudflare R2 zero egress costs
- Efficient FFmpeg command chaining
- Database indexing on foreign keys

## Security Measures
- JWT-based stateless authentication
- Password hashing with bcrypt (10 rounds)
- Helmet security headers
- CORS configuration
- Rate limiting (100 requests/15 minutes)
- Input validation
- SQL injection prevention (ORM parameterization)
- File type validation
- Signed URL expiration
- Environment variable secrets

## Error Handling
- Centralized error handler middleware
- Custom error classes (ValidationError, NotFoundError)
- 404 handler for unknown routes
- Try-catch in async routes
- Database rollback on failures
- Temporary file cleanup on errors
- User-friendly error messages

## Logging & Monitoring
- Morgan HTTP request logging (dev/combined modes)
- Console logging for video processing stages
- Error stack traces in development
- Health check endpoints for uptime monitoring
- Job queue status tracking

## Future Enhancements
- Real-time video processing progress with WebSockets
- Advanced AI features (face recognition, auto-tagging)
- Multi-language support
- Mobile apps (iOS/Android)
- Social media direct sharing
- Advanced analytics dashboard
- Collaborative editing
- Template library for compositions
- Subscription plans with feature gating
- PostgreSQL migration for production scale
