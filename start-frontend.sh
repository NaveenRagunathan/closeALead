#!/bin/bash

echo "🚀 Starting CloseALead Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    echo "VITE_API_URL=http://localhost:8000" > .env
fi

echo "✨ Starting Vite dev server on http://localhost:3000"
echo ""

npm run dev
