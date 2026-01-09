#!/bin/bash
# Setup script for Databricks Metadata Chat Assistant

set -e

echo "=========================================="
echo "Databricks Metadata Chat Assistant Setup"
echo "=========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker."
    exit 1
fi
echo "✓ Docker found"

# Check Docker Compose
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi
echo "✓ Docker Compose found"

echo ""
echo "Prerequisites check passed!"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your Azure OpenAI credentials:"
    echo "   - AZURE_OPENAI_API_KEY"
    echo "   - AZURE_OPENAI_ENDPOINT"
    echo "   - AZURE_OPENAI_DEPLOYMENT_NAME"
    echo ""
    read -p "Press Enter to continue after editing .env file..."
else
    echo "✓ .env file already exists"
fi

echo ""
echo "Starting PostgreSQL database..."
docker compose up -d

echo ""
echo "Waiting for database to be ready..."
sleep 5

# Check if database is healthy
if docker compose ps | grep -q "healthy"; then
    echo "✓ Database is running and healthy"
else
    echo "⚠️  Database is starting... waiting a bit more..."
    sleep 5
fi

echo ""
echo "Installing Python dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "Testing database connection..."
if python3 test_database.py > /dev/null 2>&1; then
    echo "✓ Database connection test passed"
else
    echo "⚠️  Database connection test failed. Retrying..."
    sleep 5
    if python3 test_database.py; then
        echo "✓ Database connection successful"
    else
        echo "❌ Database connection failed. Please check Docker logs:"
        echo "   docker compose logs postgres"
        exit 1
    fi
fi

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "To start the chat assistant, run:"
echo "  python3 main.py"
echo ""
echo "Or for detailed output:"
echo "  python3 main.py --verbose"
echo ""
echo "For help, see:"
echo "  - README.md for overview"
echo "  - USAGE.md for detailed usage instructions"
echo ""
