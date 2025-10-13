# CloseALead - AI-Powered Offer Creation Platform

Transform ordinary service offers into stunning, conversion-optimized presentations through AI-powered design and copywriting.

## 🚀 Features

- **AI-Powered Design**: ChatGPT-style conversational interface for offer creation
- **Smart Templates**: 4 conversion-tested templates (Modern, Bold, Elegant, Vibrant)
- **Live Preview**: Real-time visualization as you customize
- **Edit Tracking**: Transparent plan limits with edit counters
- **PDF Export**: High-quality presentation downloads
- **Plan Tiers**: Free, Professional, and Enterprise options
- **Redesign Tool**: Upload existing offers for instant upgrades

## 🛠️ Technology Stack

### Frontend
- **React 18** with Vite
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **React Router** for navigation
- **Axios** for API calls
- **Zustand** for state management

### Backend
- **FastAPI** (Python)
- **SQLAlchemy** with SQLite (dev) / PostgreSQL (prod)
- **JWT** authentication
- **CrewAI** for AI agent orchestration
- **OpenAI GPT-4** for content generation
- **WeasyPrint** for PDF generation
- **Stripe** for payments (optional)

## 📋 Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.11+
- **OpenAI API Key** (for AI features)

## 🔧 Installation

### 1. Clone the Repository

```bash
cd /home/letbu/Downloads/closealead
```

### 2. Frontend Setup

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Update .env with your configuration
# VITE_API_URL=http://localhost:8000
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Update .env with your settings
# Add your OpenAI API key
```

### 4. Database Initialization

```bash
# Backend automatically creates SQLite database on first run
# For production, configure PostgreSQL in .env
```

## 🚀 Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
# Backend will run on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
npm run dev
# Frontend will run on http://localhost:3000
```

### Production Build

**Frontend:**
```bash
npm run build
# Creates optimized build in dist/
```

**Backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📁 Project Structure

```
closealead/
├── backend/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── offers.py        # Offer CRUD operations
│   │       └── users.py         # User management
│   ├── core/
│   │   ├── config.py            # Configuration settings
│   │   ├── database.py          # Database connection
│   │   └── security.py          # JWT & password hashing
│   ├── crew/
│   │   ├── agents.py            # CrewAI agent definitions
│   │   ├── tasks.py             # CrewAI task definitions
│   │   └── crews.py             # Crew orchestration
│   ├── models/
│   │   ├── user.py              # User database model
│   │   └── offer.py             # Offer database model
│   ├── services/
│   │   └── pdf_service.py       # PDF generation
│   ├── main.py                  # FastAPI application
│   └── requirements.txt         # Python dependencies
├── src/
│   ├── components/
│   │   ├── auth/                # Login & Signup modals
│   │   ├── creator/             # Offer creator components
│   │   ├── dashboard/           # Dashboard components
│   │   └── landing/             # Landing page components
│   ├── contexts/
│   │   └── AuthContext.jsx      # Authentication state
│   ├── pages/
│   │   ├── Dashboard.jsx        # User dashboard
│   │   ├── LandingPage.jsx      # Marketing page
│   │   └── OfferCreator.jsx     # Offer creation flow
│   ├── services/
│   │   └── api.js               # API client
│   ├── App.jsx                  # Main app component
│   └── main.jsx                 # Entry point
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## 🔑 Environment Variables

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```env
# Database
DATABASE_URL=sqlite:///./closealead.db

# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION=86400

# OpenAI (Required for AI features)
OPENAI_API_KEY=sk-your-api-key-here

# Optional: AWS for file storage
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
S3_BUCKET=

# Optional: Stripe for payments
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
```

## 🎯 Usage Guide

### Creating Your First Offer

1. **Sign Up**: Create a free account
2. **Choose Mode**: 
   - "Create From Scratch" - AI guides you through questions
   - "Redesign Existing" - Upload your current offer
3. **AI Conversation**: Answer questions about your service
4. **Select Template**: Choose from 4 professional styles
5. **Customize**: Fine-tune content, colors, and branding
6. **Export**: Download as high-quality PDF

### Plan Limits

| Feature | Free | Professional | Enterprise |
|---------|------|--------------|------------|
| Active Offers | 1 | 4 | Unlimited |
| Edits per Offer | 5 | 15 | Unlimited |
| Templates | All 4 | All 4 | All 4 + Custom |
| PDF Export | ✓ | ✓ | ✓ (No watermark) |
| Priority Support | - | ✓ | ✓ |

## 🧪 Testing

### Frontend Tests
```bash
npm run test
```

### Backend Tests
```bash
cd backend
pytest
```

## 📊 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/v1/auth/signup` - Create account
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/offers` - List user offers
- `POST /api/v1/offers` - Create new offer
- `PUT /api/v1/offers/{id}` - Update offer
- `POST /api/v1/offers/{id}/export` - Export PDF

## 🔒 Security Features

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: bcrypt with salt rounds
- **CORS Protection**: Configured origins only
- **Rate Limiting**: API endpoint protection
- **Input Validation**: Pydantic models
- **SQL Injection Prevention**: SQLAlchemy ORM

## 🚢 Deployment

### Frontend (Vercel/Netlify)

```bash
npm run build
# Deploy dist/ folder
```

### Backend (Railway/Render/AWS)

```bash
# Use provided Dockerfile or direct deployment
# Set environment variables in platform
```

### Database (Production)

Replace SQLite with PostgreSQL:
```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Backend won't start
- Check Python version (3.11+)
- Verify all dependencies installed
- Ensure .env file exists with valid values

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check VITE_API_URL in .env
- Check CORS settings in backend

### AI features not working
- Verify OPENAI_API_KEY is set in backend/.env
- Check OpenAI API quota/billing
- Review backend logs for errors

### Database errors
- Delete closealead.db and restart (dev only)
- Check DATABASE_URL format
- Ensure write permissions

## 📧 Support

For issues and questions:
- GitHub Issues: [Create Issue](https://github.com/yourusername/closealead/issues)
- Email: support@closealead.com
- Documentation: [Full Docs](https://docs.closealead.com)

## 🎉 Credits

Built with ❤️ using:
- React & Vite
- FastAPI & Python
- CrewAI for AI orchestration
- OpenAI GPT-4
- Tailwind CSS
- Framer Motion

---

**Made with CloseALead** - Turn Your Offers Into Irresistible Presentations That Close
