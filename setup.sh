#!/bin/bash

echo "🚀 Setting up CloseALead..."

# Frontend setup
echo "📦 Frontend dependencies already installed"

# Backend setup
echo "🐍 Setting up Python backend..."
cd backend

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating backend .env file..."
    cat > .env << EOL
# Database
DATABASE_URL=sqlite:///./closealead.db

# Security
SECRET_KEY=dev-secret-key-change-in-production

# OpenAI (Add your key here)
OPENAI_API_KEY=

# CORS
CORS_ORIGINS=http://localhost:3000
EOL
    echo "✅ Created backend/.env"
    echo "⚠️  Please add your OPENAI_API_KEY to backend/.env for AI features"
fi

# Install Python dependencies
if [ -d "venv" ]; then
    echo "✅ Virtual environment exists"
    source venv/bin/activate
    echo "📦 Installing Python dependencies..."
    pip install -q -r requirements.txt
    echo "✅ Python dependencies installed"
else
    echo "❌ Virtual environment not found. Run: python3 -m venv venv"
fi

cd ..

# Create frontend .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating frontend .env file..."
    echo "VITE_API_URL=http://localhost:8000" > .env
    echo "✅ Created .env"
fi

echo ""
echo "✨ Setup complete! ✨"
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  npm run dev"
echo ""
echo "Then open http://localhost:3000"
echo ""
