# 🧪 CloseALead Testing Guide

## Manual Testing Checklist

### 1. Authentication Flow

#### Sign Up
- [ ] Open http://localhost:3000
- [ ] Click "Get Started Free" or "Sign Up"
- [ ] Enter name (min 2 characters)
- [ ] Enter valid email
- [ ] Enter password (8+ chars, 1 uppercase, 1 number)
- [ ] Confirm password matches
- [ ] Select plan (Free/Professional/Enterprise)
- [ ] Check "Agree to Terms"
- [ ] Click "Create Account"
- [ ] ✅ Should redirect to dashboard
- [ ] ✅ Should see welcome message with name

#### Login
- [ ] Click "Login" or "Log In"
- [ ] Enter registered email
- [ ] Enter correct password
- [ ] Click "Remember Me" (optional)
- [ ] Click "Log In"
- [ ] ✅ Should redirect to dashboard
- [ ] ✅ Should see user's existing offers

#### Logout
- [ ] Click "Logout" button
- [ ] ✅ Should redirect to landing page
- [ ] ✅ Should clear session

### 2. Dashboard Functionality

#### Statistics Cards
- [ ] **Total Offers Card**
  - [ ] Shows correct count
  - [ ] Shows limit (Free: 1, Pro: 4, Enterprise: ∞)
  - [ ] Progress bar updates correctly
  - [ ] Turns red when > 80% used

- [ ] **Current Plan Card**
  - [ ] Shows correct plan badge
  - [ ] Shows "Upgrade" button (not for Enterprise)
  - [ ] Correct color coding

- [ ] **Edits Remaining Card**
  - [ ] Shows total edits across all offers
  - [ ] Updates when offers are edited
  - [ ] Warning when < 10 edits left

#### Offer Grid
- [ ] Empty state shows when no offers
- [ ] "Create Your First Offer" button works
- [ ] Offers display in grid layout
- [ ] Each card shows:
  - [ ] Title and subtitle preview
  - [ ] Creation date
  - [ ] Edit count and limit
  - [ ] Progress bar
  - [ ] Template badge
- [ ] Hover effect on cards
- [ ] Edit button opens editor
- [ ] View button shows preview
- [ ] Delete button prompts confirmation

### 3. Offer Creation - From Scratch

#### Mode Selection
- [ ] Click "Create New Offer"
- [ ] See two mode options
- [ ] Click "Create From Scratch"
- [ ] ✅ Should load AI chat interface

#### AI Chat Conversation
Test all 8 questions:

1. **Service/Product**
   - [ ] Type answer (e.g., "Social Media Marketing")
   - [ ] Press Enter or click Send
   - [ ] ✅ AI responds with next question

2. **Target Audience**
   - [ ] Type specific audience
   - [ ] ✅ AI acknowledges and continues

3. **Problem Solved**
   - [ ] Describe main pain point
   - [ ] ✅ AI progresses

4. **Price Point**
   - [ ] Enter price (e.g., "997")
   - [ ] ✅ AI continues

5. **Key Features**
   - [ ] List 3+ features
   - [ ] ✅ AI proceeds

6. **Unique Value**
   - [ ] Describe differentiation
   - [ ] ✅ AI asks next

7. **Guarantees/Bonuses**
   - [ ] List any guarantees
   - [ ] ✅ AI continues

8. **Brand Personality**
   - [ ] Choose: professional/friendly/bold/luxurious
   - [ ] ✅ AI processes and shows "Creating your offer..."
   - [ ] ✅ Redirects to template selection

#### Template Selection
- [ ] See 4 template cards
- [ ] **Modern Template**
  - [ ] Preview shows gradient
  - [ ] Click to select
  - [ ] Check mark appears

- [ ] **Bold Template**
  - [ ] High contrast preview
  - [ ] Selectable

- [ ] **Elegant Template**
  - [ ] Navy/gold preview
  - [ ] Selectable

- [ ] **Vibrant Template**
  - [ ] Colorful preview
  - [ ] Selectable

- [ ] Click "Continue with [Template]"
- [ ] ✅ Loads customization panel

### 4. Offer Customization

#### Content Section
- [ ] Edit title (max 60 chars)
  - [ ] Character counter updates
  - [ ] Prevents typing beyond limit
- [ ] Edit subtitle (max 120 chars)
  - [ ] Character counter works
- [ ] Edit description (rich text)
  - [ ] Word count shows
  - [ ] Multi-line editing works
- [ ] ✅ Live preview updates in real-time

#### Pricing Section
- [ ] Change price amount
- [ ] Select currency (USD/EUR/GBP/CAD)
- [ ] Choose interval:
  - [ ] One-time
  - [ ] Monthly
  - [ ] Annually
- [ ] ✅ Preview shows correct currency symbol
- [ ] ✅ Preview shows correct interval text

#### Features Section
- [ ] Add feature (click "+ Add Feature")
- [ ] Edit feature text
- [ ] Reorder features (if drag-drop implemented)
- [ ] Remove feature (click X)
- [ ] Maximum 10 features enforced
- [ ] ✅ Live preview shows all features

#### Branding Section
- [ ] Enter logo URL
  - [ ] Preview updates (if valid URL)
- [ ] **Primary Color**
  - [ ] Click color picker
  - [ ] Choose color
  - [ ] Manual hex input works
  - [ ] ✅ Preview applies color
- [ ] **Secondary Color**
  - [ ] Color picker works
  - [ ] Updates preview
- [ ] **Accent Color**
  - [ ] Color picker works
  - [ ] Updates preview

#### Images Section
- [ ] Enter hero image URL
- [ ] Upload button present (placeholder)

#### Live Preview
- [ ] **Preview Panel (Right Side)**
  - [ ] Shows selected template
  - [ ] Updates in real-time
  - [ ] Scrollable for long content
  - [ ] Zoom controls work

- [ ] **Modern Template Preview**
  - [ ] Blue gradient header
  - [ ] Clean layout
  - [ ] Features with checkmarks
  - [ ] Pricing box centered

- [ ] **Bold Template Preview**
  - [ ] Black background
  - [ ] Red accents
  - [ ] High contrast

- [ ] **Elegant Template Preview**
  - [ ] Navy blue
  - [ ] Gold accents
  - [ ] Sophisticated

- [ ] **Vibrant Template Preview**
  - [ ] Colorful gradients
  - [ ] Energetic feel

### 5. Edit Tracking

#### Edit Counter
- [ ] Shows "Edits: X/Y" in header
- [ ] Counter at 0 initially
- [ ] Increments after changes
- [ ] Progress circle updates
- [ ] Color changes:
  - [ ] Green: > 50% remaining
  - [ ] Yellow: 20-50% remaining
  - [ ] Red: < 20% remaining

#### Limit Reached
- [ ] Make edits until limit reached
- [ ] Warning modal appears
- [ ] Options shown:
  - [ ] Save as is
  - [ ] Upgrade plan
  - [ ] Delete and start over

### 6. Save & Export

#### Save Draft
- [ ] Click "Save Draft"
- [ ] ✅ Success toast appears
- [ ] ✅ Offer saved to database
- [ ] ✅ Can navigate away and return

#### Export PDF
- [ ] Click "Export as PDF"
- [ ] ✅ Loading indicator shows
- [ ] ✅ PDF downloads automatically
- [ ] ✅ Filename correct
- [ ] Open PDF and verify:
  - [ ] All content present
  - [ ] Template style applied
  - [ ] Colors correct
  - [ ] Features formatted
  - [ ] Pricing displayed
  - [ ] Professional quality

### 7. Offer Redesign Flow

#### File Upload
- [ ] Click "Create New Offer"
- [ ] Select "Redesign Existing"
- [ ] See upload zone
- [ ] **Drag & Drop**
  - [ ] Drag PDF file
  - [ ] Drop zone highlights
  - [ ] File accepted
- [ ] **Browse Upload**
  - [ ] Click "Browse Files"
  - [ ] Select PDF/DOCX/TXT
  - [ ] File shows in UI
- [ ] **Validation**
  - [ ] Rejects invalid formats
  - [ ] Rejects files > 10MB
- [ ] Click "Process & Redesign"
- [ ] ✅ Shows processing animation
- [ ] ✅ Extracts content
- [ ] ✅ Proceeds to template selection

### 8. Plan Limits Enforcement

#### Free Plan (1 offer, 5 edits)
- [ ] Can create 1 offer
- [ ] Creating 2nd offer blocked
- [ ] Shows upgrade prompt
- [ ] Each offer has 5 edit limit
- [ ] Editing beyond limit blocked

#### Professional Plan (4 offers, 15 edits)
- [ ] Can create up to 4 offers
- [ ] 5th offer blocked
- [ ] Each offer has 15 edits
- [ ] Higher limits shown in dashboard

#### Enterprise Plan (Unlimited)
- [ ] No offer limit shown
- [ ] Unlimited edits shown as "∞"
- [ ] No restrictions

### 9. Responsive Design

#### Mobile (< 768px)
- [ ] Navigation hamburger menu works
- [ ] Landing page readable
- [ ] Dashboard cards stack vertically
- [ ] Offer creator usable
- [ ] Modals fit screen
- [ ] Touch interactions work

#### Tablet (768px - 1024px)
- [ ] Layout adjusts appropriately
- [ ] Grid shows 2 columns
- [ ] Readable and usable

#### Desktop (> 1024px)
- [ ] Full layout displays
- [ ] Customization panel + preview side-by-side
- [ ] Grid shows 3 columns
- [ ] Optimal spacing

### 10. Error Handling

#### Network Errors
- [ ] Disconnect internet
- [ ] Try to create offer
- [ ] ✅ Error toast appears
- [ ] ✅ Graceful fallback

#### Invalid Data
- [ ] Submit empty form
- [ ] ✅ Validation errors show
- [ ] Submit malformed email
- [ ] ✅ Email validation works

#### Authentication Errors
- [ ] Login with wrong password
- [ ] ✅ "Invalid credentials" message
- [ ] Access protected route without login
- [ ] ✅ Redirects to home

### 11. Performance

#### Load Times
- [ ] Landing page < 2s
- [ ] Dashboard < 1s (after auth)
- [ ] Offer creator < 1s
- [ ] PDF export < 5s

#### Interactions
- [ ] UI feels responsive
- [ ] No lag on typing
- [ ] Smooth animations
- [ ] No console errors

### 12. Browser Compatibility

Test in:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### 13. Accessibility

- [ ] Keyboard navigation works
- [ ] Tab order logical
- [ ] Enter submits forms
- [ ] Escape closes modals
- [ ] Focus indicators visible
- [ ] Alt text on images (when added)

---

## Backend API Testing

### Using Swagger UI (http://localhost:8000/docs)

#### Authentication Endpoints
```
POST /api/v1/auth/signup
Body: { name, email, password, plan }
Expected: 201, returns user + token

POST /api/v1/auth/login
Body: { email, password }
Expected: 200, returns user + token
```

#### Offers Endpoints
```
GET /api/v1/offers
Headers: Authorization: Bearer {token}
Expected: 200, returns array of offers

POST /api/v1/offers
Headers: Authorization: Bearer {token}
Body: { offer data }
Expected: 201, returns created offer

PUT /api/v1/offers/{id}
Headers: Authorization: Bearer {token}
Body: { updated fields }
Expected: 200, returns updated offer

DELETE /api/v1/offers/{id}
Headers: Authorization: Bearer {token}
Expected: 204, no content
```

---

## Automated Testing (Future)

### Frontend Unit Tests
```bash
npm run test
```

### Backend Tests
```bash
cd backend
pytest
```

---

## Bug Reporting Template

When you find a bug, report with:

```
**Bug Title**: Brief description

**Steps to Reproduce**:
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**: What should happen

**Actual Behavior**: What actually happened

**Environment**:
- Browser: Chrome 120
- OS: Ubuntu 22.04
- Node: v18.17.0
- Python: 3.11.0

**Screenshots**: (if applicable)

**Console Errors**: (paste here)
```

---

## Test Data

### Sample User
```
Name: John Doe
Email: john@example.com
Password: TestPass123
Plan: professional
```

### Sample Offer
```
Title: Social Media Marketing Services
Subtitle: Grow your brand on Instagram, Facebook, and TikTok
Price: $997/month
Features:
- Daily content creation
- Community management
- Analytics reporting
- Influencer outreach
- Ad campaign management
```

---

**Happy Testing! 🧪**
