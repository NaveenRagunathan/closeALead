# CloseALead Architecture Documentation

## System Overview

CloseALead is a full-stack web application that uses AI to transform service offers into professionally designed presentations.

## High-Level Architecture

```
┌─────────────┐
│   Browser   │
│  (React)    │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────┐
│   Vite Dev Server   │
│   (Development)     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   FastAPI Backend   │
│   (Port 8000)       │
└──────┬──────────────┘
       │
   ┌───┴────┬─────────────┐
   ▼        ▼             ▼
┌────┐  ┌──────┐    ┌────────┐
│Auth│  │Offers│    │ CrewAI │
│    │  │      │    │ Engine │
└─┬──┘  └───┬──┘    └───┬────┘
  │         │           │
  ▼         ▼           ▼
┌──────────────────────────┐
│     SQLite Database      │
└──────────────────────────┘
```

## Frontend Architecture

### Component Hierarchy

```
App
├── AuthProvider (Context)
├── Router
    ├── LandingPage
    │   ├── Navigation
    │   ├── Hero
    │   ├── Features
    │   └── Pricing
    ├── Dashboard (Protected)
    │   ├── StatCards
    │   └── OfferGrid
    │       └── OfferCard[]
    └── OfferCreator (Protected)
        ├── ModeSelector
        ├── AIChat
        ├── FileUpload
        ├── TemplateSelector
        ├── CustomizationPanel
        └── LivePreview
```

### State Management

**Authentication State (Context)**
```javascript
{
  user: {
    id, name, email, plan, offerCount
  },
  isAuthenticated: boolean,
  login(), signup(), logout()
}
```

**Offer State (Component)**
```javascript
{
  title, subtitle, description,
  price: { amount, currency, interval },
  features: [],
  template: "modern|bold|elegant|vibrant",
  brandColors: { primary, secondary, accent },
  editCount, editLimit
}
```

### Routing

- `/` - Landing page (public)
- `/dashboard` - User dashboard (protected)
- `/create` - New offer creator (protected)
- `/edit/:offerId` - Edit existing offer (protected)

## Backend Architecture

### API Layer

**FastAPI Application Structure**
```python
main.py
├── CORS Middleware
├── Router: /api/v1/auth
│   ├── POST /signup
│   └── POST /login
├── Router: /api/v1/offers
│   ├── GET /
│   ├── GET /{id}
│   ├── POST /
│   ├── PUT /{id}
│   ├── DELETE /{id}
│   └── POST /{id}/export
└── Router: /api/v1/users
    └── GET /profile
```

### Database Schema

**Users Table**
```sql
id: UUID (PK)
name: String
email: String (UNIQUE)
password_hash: String
plan: Enum(free, professional, enterprise)
stripe_customer_id: String (nullable)
subscription_ends_at: DateTime (nullable)
created_at: DateTime
updated_at: DateTime
```

**Offers Table**
```sql
id: UUID (PK)
user_id: UUID (FK -> users.id)
title: String(200)
subtitle: String(300)
description: Text
price_amount: Float
price_currency: String(3)
price_interval: String(20)
features: JSON
template: String(50)
brand_colors: JSON
logo_url: String(500)
images: JSON
edit_count: Integer
edit_limit: Integer
created_at: DateTime
updated_at: DateTime
pdf_url: String(500)
```

### Security Layer

**JWT Authentication Flow**
```
1. User submits credentials
2. Backend verifies password (bcrypt)
3. Generate JWT token (HS256)
4. Return token to client
5. Client stores token in localStorage
6. Client sends token in Authorization header
7. Backend validates token on protected routes
```

**Password Security**
- Algorithm: bcrypt
- Salt rounds: 12
- Minimum: 8 chars, 1 uppercase, 1 number

### CrewAI Integration

**Agent Architecture**
```python
Information Gatherer
├── Role: Extract offer details
├── Model: GPT-4-Turbo
└── Output: Structured JSON

Copywriter
├── Role: Create compelling copy
├── Model: GPT-4-Turbo
└── Output: Persuasive content

Design Strategist
├── Role: Visual recommendations
├── Model: GPT-4-Turbo
└── Output: Template + color palette

Quality Assurance
├── Role: Validate completeness
├── Model: GPT-4-Turbo
└── Output: Quality score + feedback
```

**Crew Execution Flow**
```
1. User provides input
2. Information Gatherer processes
3. Copywriter enhances
4. Design Strategist recommends
5. Quality Assurance validates
6. Return final offer data
```

### PDF Generation

**WeasyPrint Flow**
```
1. Receive offer data
2. Select template HTML
3. Inject offer content
4. Apply CSS styling
5. Generate PDF binary
6. Return as download
```

**Template System**
- Modern: Blue gradient, clean lines
- Bold: High contrast, statement design
- Elegant: Luxury gold accents
- Vibrant: Colorful gradients

## Data Flow

### Offer Creation Flow

```
User Input
    ↓
AI Chat Component
    ↓
POST /api/v1/offers (with AI-processed data)
    ↓
Backend validates plan limits
    ↓
Create offer in database
    ↓
Return offer ID
    ↓
Redirect to /edit/{offerId}
    ↓
Customization Panel + Live Preview
    ↓
PUT /api/v1/offers/{id} (on changes)
    ↓
Update database (increment edit_count)
    ↓
POST /api/v1/offers/{id}/export
    ↓
Generate PDF via WeasyPrint
    ↓
Download to user
```

## Plan Enforcement

**Limits Matrix**
```javascript
{
  free: { offers: 1, edits: 5 },
  professional: { offers: 4, edits: 15 },
  enterprise: { offers: ∞, edits: ∞ }
}
```

**Enforcement Points**
1. Offer creation: Check count < limit
2. Offer update: Check edit_count < edit_limit
3. Frontend: Disable buttons when limit reached
4. Backend: Return 403 if limit exceeded

## Error Handling

**Frontend**
- Toast notifications for user feedback
- Graceful fallbacks on API errors
- Loading states during async operations

**Backend**
- HTTP status codes (400, 401, 403, 404, 500)
- Detailed error messages in response
- Exception logging
- Global exception handler

## Performance Considerations

**Frontend**
- Code splitting by route
- Lazy loading of components
- Image optimization
- Debounced edit tracking (5s)

**Backend**
- Database connection pooling
- SQLAlchemy query optimization
- Async endpoints where applicable
- PDF generation caching (future)

## Security Measures

1. **Authentication**: JWT with short expiry
2. **Authorization**: User-specific data access
3. **Input Validation**: Pydantic models
4. **SQL Injection**: SQLAlchemy ORM
5. **XSS Protection**: React auto-escaping
6. **CORS**: Restricted origins
7. **Rate Limiting**: Future enhancement

## Scalability Path

**Current (MVP)**
- Single server
- SQLite database
- In-memory sessions

**Future (Production)**
- Load balancer
- PostgreSQL with read replicas
- Redis for caching
- S3 for file storage
- Celery for background jobs
- WebSocket for real-time AI chat

## Monitoring & Logging

**Current**
- Console logs
- FastAPI automatic docs
- React DevTools

**Future**
- Sentry for error tracking
- Prometheus for metrics
- CloudWatch for AWS
- Structured logging (JSON)

---

This architecture is designed to be:
- **Scalable**: Easy to add workers, databases
- **Maintainable**: Clear separation of concerns
- **Secure**: Multiple security layers
- **User-friendly**: Fast, responsive, intuitive
