# 🚀 CloseALead Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies

### Frontend
```bash
npm install
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Configure Environment

### Frontend
```bash
# Create .env file in root directory
echo "VITE_API_URL=http://localhost:8000" > .env
```

### Backend
```bash
# Create .env file in backend directory
cd backend
cp .env.example .env

# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here
```

## Step 3: Start the Application

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
python main.py
```

You should see:
```
🚀 Starting CloseALead API Server...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 - Frontend
```bash
npm run dev
```

You should see:
```
VITE v5.0.0  ready in 500 ms
➜  Local:   http://localhost:3000/
```

## Step 4: Open Application

Navigate to: **http://localhost:3000**

## Step 5: Create Your First Offer

1. Click **"Get Started Free"**
2. Sign up with your email
3. Click **"Create New Offer"**
4. Choose **"Create From Scratch"**
5. Answer the AI's questions
6. Select a template
7. Customize and export!

## 🎉 You're Done!

### Next Steps:
- Explore all 4 templates
- Try the "Redesign Existing" mode
- Customize colors and branding
- Export your first PDF

### Need Help?
- Check the full README.md
- Visit API docs at http://localhost:8000/docs
- Review troubleshooting section

## Common Issues

**Backend won't start?**
- Make sure Python 3.11+ is installed
- Check that port 8000 is available
- Verify .env file exists in backend/

**Frontend errors?**
- Run `npm install` again
- Clear cache: `rm -rf node_modules package-lock.json && npm install`
- Check that backend is running

**Can't sign up?**
- Check backend terminal for errors
- Verify database file is created (backend/closealead.db)
- Try different email/password

---

**Happy Creating! 🎨**
