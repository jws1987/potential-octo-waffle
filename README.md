# Databricks Metadata Chat Assistant

A CLI-only chat assistant powered by LangChain and Azure OpenAI that helps you query Databricks catalog metadata using natural language.

## 🌟 Features

- **Natural Language Queries**: Ask questions about your Databricks metadata in plain English
- **Azure OpenAI Integration**: Powered by Azure OpenAI for intelligent query understanding
- **LangChain SQL Agent**: Automatic conversion from natural language to SQL queries
- **Safety First**: Read-only queries with built-in query validation and limits
- **PostgreSQL Backend**: Lightweight PostgreSQL database hosting Databricks metadata replica
- **Docker Support**: Easy local setup with Docker Compose
- **Interactive CLI**: User-friendly command-line interface

## 📋 Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose
- Azure OpenAI account with API access
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/jws1987/potential-octo-waffle.git
cd potential-octo-waffle
```

### 2. Set Up Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and add your Azure OpenAI credentials:

```env
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2023-12-01-preview
```

**Note:** The PostgreSQL credentials are already set to use the read-only user (`readonly_user`) created by the initialization script. You don't need to change these unless you modify the database setup.

### 3. Start PostgreSQL Database

```bash
docker-compose up -d
```

This will:
- Start a PostgreSQL 16 container
- Initialize the database with Databricks metadata schema
- Load sample data for testing
- Create a read-only user for the application

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Chat Assistant

```bash
python main.py
```

## 💬 Usage

Once the application starts, you'll see an interactive prompt. You can:

### Ask Natural Language Questions

```
💬 You: What tables are in the sales schema?
💬 You: Show me all columns in the orders table
💬 You: List all catalogs and their owners
💬 You: Which tables contain customer information?
```

### Use Special Commands

- `schema` - Display the complete database schema
- `help` - Show help information
- `quit` or `exit` - Exit the application

### Example Session

```
╔══════════════════════════════════════════════════════════════╗
║   Databricks Metadata Chat Assistant                        ║
║   Powered by LangChain & Azure OpenAI                        ║
╚══════════════════════════════════════════════════════════════╝

💬 You: What tables exist in the main catalog?

🤔 Thinking...

======================================================================
📊 Answer:
In the main catalog, there are 5 tables:
1. sales.orders - Customer orders table
2. sales.order_items - Order line items
3. sales.products - Product catalog
4. customer.customers - Customer information
5. customer.addresses - Customer addresses
======================================================================
```

## 🏗️ Architecture

### Components

1. **CLI Interface** (`src/cli.py`): Interactive command-line interface
2. **LangChain Agent** (`src/agent.py`): Natural language to SQL conversion
3. **Database Manager** (`src/database.py`): Safe query execution and connection management
4. **Configuration** (`src/config.py`): Settings and environment variable management

### Data Flow

```
User Question
    ↓
CLI Interface
    ↓
LangChain SQL Agent (Azure OpenAI)
    ↓
SQL Query Generation
    ↓
Database Manager (Safety Checks)
    ↓
PostgreSQL (Read-Only)
    ↓
Results → Formatted Answer
    ↓
CLI Display
```

## 🗄️ Database Schema

The PostgreSQL database contains four main tables that mirror Databricks information_schema:

### catalogs
- `catalog_name` (PK)
- `catalog_owner`
- `comment`
- `created_at`

### schemas
- `catalog_name` (PK, FK)
- `schema_name` (PK)
- `schema_owner`
- `comment`
- `created_at`

### tables
- `table_catalog` (PK, FK)
- `table_schema` (PK, FK)
- `table_name` (PK)
- `table_type`
- `table_owner`
- `comment`
- `created_at`

### columns
- `table_catalog` (PK, FK)
- `table_schema` (PK, FK)
- `table_name` (PK, FK)
- `column_name` (PK)
- `ordinal_position`
- `data_type`
- `is_nullable`
- `column_default`
- `comment`

## 🔒 Security Features

1. **Read-Only Database User**: Application uses a dedicated read-only user
2. **Query Validation**: Blocks INSERT, UPDATE, DELETE, and DDL statements
3. **Query Limits**: Automatic LIMIT clause added to prevent excessive results
4. **Connection Pooling**: Controlled database connections
5. **Error Handling**: Graceful error handling and logging

## 🛠️ Development

### Project Structure

```
.
├── docker-compose.yml          # Docker configuration
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── sql/
│   └── init.sql               # Database initialization script
└── src/
    ├── __init__.py
    ├── agent.py               # LangChain agent
    ├── cli.py                 # CLI interface
    ├── config.py              # Configuration management
    └── database.py            # Database management
```

### Adding Custom Data

To populate the database with your own Databricks metadata:

1. Export your Databricks information_schema tables
2. Transform the data to match the PostgreSQL schema
3. Load it using SQL INSERT statements or a data loading script

### Customizing the Agent

Edit `src/agent.py` to:
- Modify the LLM temperature for creativity vs. consistency
- Adjust max iterations for complex queries
- Customize the system prompt and context

## 🐛 Troubleshooting

### Database Connection Failed

```bash
# Check if PostgreSQL is running
docker-compose ps

# View PostgreSQL logs
docker-compose logs postgres

# Restart the database
docker-compose restart postgres
```

### Azure OpenAI Authentication Error

- Verify your API key in `.env`
- Check that your endpoint URL is correct
- Ensure your deployment name matches your Azure OpenAI deployment

### Module Not Found Error

```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

## 📝 License

This project is provided as-is for demonstration purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Support

For questions or issues, please open an issue on GitHub.