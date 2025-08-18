#!/bin/bash
# CogniBot Docker Test Script for Rancher Desktop
# Tests the Docker setup locally

set -e

echo "🐳 Testing CogniBot Docker Setup with Rancher Desktop"
echo "===================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Rancher Desktop / Docker
echo "📋 Checking prerequisites..."

if command_exists docker; then
    echo "✅ Docker found: $(docker --version)"
else
    echo "❌ Docker not found. Make sure Rancher Desktop is running."
    exit 1
fi

if command_exists docker-compose; then
    echo "✅ Docker Compose found: $(docker-compose --version)"
else
    echo "❌ Docker Compose not found."
    exit 1
fi

# Check if Rancher Desktop is running
if docker info >/dev/null 2>&1; then
    echo "✅ Docker daemon is running"
else
    echo "❌ Docker daemon not running. Start Rancher Desktop first."
    exit 1
fi

# Check .env file
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env_template.txt .env
    echo "⚠️  IMPORTANT: Edit .env file with your credentials!"
    echo "   Required: TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, TELEGRAM_CHANNELS"
    echo ""
    echo "❌ Please configure .env file and run this script again."
    exit 1
else
    echo "✅ .env file exists"
fi

# Create logs directory
mkdir -p logs
echo "✅ Logs directory ready"

# Test Docker build
echo ""
echo "🏗️  Testing Docker build..."
if docker-compose build; then
    echo "✅ Docker build successful"
else
    echo "❌ Docker build failed"
    exit 1
fi

# Check if we have valid config (basic check)
echo ""
echo "🔍 Checking configuration..."
if grep -q "your_telegram_bot_token_here" .env; then
    echo "⚠️  Warning: .env still contains template values"
    echo "   The bot won't work until you add real credentials"
    echo "   But Docker setup is working correctly!"
else
    echo "✅ .env appears to be configured"
fi

echo ""
echo "🎉 Docker setup test completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Configure your .env file with real credentials"
echo "2. Start the bot: docker-compose up -d"
echo "3. View logs: docker-compose logs -f cognibot"
echo "4. Stop the bot: docker-compose down"
echo ""
echo "🖥️  You can also monitor containers in Rancher Desktop UI" 