# Usage Guide

This guide provides detailed instructions for using the Databricks Metadata Chat Assistant.

## Initial Setup

### 1. Prerequisites Check

Before starting, ensure you have:
- Python 3.9+ installed: `python --version`
- Docker installed: `docker --version`
- Git installed: `git --version`

### 2. Environment Setup

Create a `.env` file from the example:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```bash
nano .env  # or use your preferred editor
```

Required settings:
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_DEPLOYMENT_NAME`: Your deployment name

### 3. Start the Database

Start PostgreSQL using Docker Compose:
```bash
docker compose up -d
```

Verify it's running:
```bash
docker compose ps
```

You should see `databricks_metadata_db` running.

### 4. Install Dependencies

Install Python packages:
```bash
pip install -r requirements.txt
```

### 5. Verify Setup

Test the database connection:
```bash
python test_database.py
```

## Running the Chat Assistant

Start the interactive CLI:
```bash
python main.py
```

You'll see the welcome banner:
```
╔══════════════════════════════════════════════════════════════╗
║   Databricks Metadata Chat Assistant                        ║
║   Powered by LangChain & Azure OpenAI                        ║
╚══════════════════════════════════════════════════════════════╝
```

## Using the Chat Assistant

### Natural Language Queries

Ask questions in plain English:

**Example 1: List tables**
```
💬 You: What tables are in the sales schema?
```

**Example 2: Column information**
```
💬 You: Show me all columns in the customers table
```

**Example 3: Find related tables**
```
💬 You: Which tables contain information about orders?
```

**Example 4: Metadata queries**
```
💬 You: Who owns the analytics catalog?
```

**Example 5: Data type queries**
```
💬 You: What are the data types for columns in the orders table?
```

**Example 6: Complex queries**
```
💬 You: List all tables with their column counts
```

### Special Commands

#### Show Schema
Display the complete database schema:
```
💬 You: schema
```

#### Get Help
Show available commands and examples:
```
💬 You: help
```

#### Exit
Exit the application:
```
💬 You: quit
```
or
```
💬 You: exit
```

## Query Examples

### Catalog Exploration
```
💬 You: List all catalogs
💬 You: Show me catalogs owned by the analytics team
💬 You: How many catalogs exist?
```

### Schema Discovery
```
💬 You: What schemas exist in the main catalog?
💬 You: Show me all schemas with their owners
💬 You: Which schemas are in the dev catalog?
```

### Table Queries
```
💬 You: List all tables in main.sales
💬 You: What's the description of the orders table?
💬 You: Show me all VIEW type tables
💬 You: Which tables are owned by the sales_team?
```

### Column Analysis
```
💬 You: What columns does the customers table have?
💬 You: Show me all BIGINT columns across all tables
💬 You: Which columns allow NULL values in the orders table?
💬 You: List columns with comments in the products table
```

### Cross-Table Queries
```
💬 You: Find tables that might be related to customers
💬 You: Show me all tables with their column counts
💬 You: List all foreign key relationships
```

## Understanding the Output

The assistant provides structured answers:

```
======================================================================
📊 Answer:
The sales schema in the main catalog contains 3 tables:
1. orders - Customer orders table
2. order_items - Order line items
3. products - Product catalog
======================================================================
```

If an error occurs:
```
======================================================================
❌ Error: Could not find the specified table
======================================================================
```

## Tips for Better Results

### Be Specific
❌ Bad: "Show me data"
✅ Good: "Show me all tables in the sales schema"

### Use Context
❌ Bad: "What columns?"
✅ Good: "What columns are in the customers table?"

### Ask Follow-ups
You can ask follow-up questions based on previous answers:
```
💬 You: What tables are in main.sales?
🤔 Answer: orders, order_items, products

💬 You: Show me the columns in the orders table
```

## Troubleshooting

### "Failed to initialize"
**Problem**: Can't connect to database or Azure OpenAI

**Solutions**:
1. Check if PostgreSQL is running:
   ```bash
   docker compose ps
   ```

2. Verify `.env` file exists and has correct credentials

3. Test database connection:
   ```bash
   python test_database.py
   ```

### "Database connection failed"
**Problem**: Can't reach PostgreSQL

**Solutions**:
1. Restart the database:
   ```bash
   docker compose restart postgres
   ```

2. Check logs:
   ```bash
   docker compose logs postgres
   ```

3. Verify port 5432 is not in use:
   ```bash
   lsof -i :5432
   ```

### "Azure OpenAI authentication error"
**Problem**: Invalid Azure OpenAI credentials

**Solutions**:
1. Verify your API key in `.env`
2. Check endpoint URL format (should end with `.azure.com/`)
3. Confirm deployment name matches your Azure OpenAI setup
4. Test credentials in Azure Portal

### "Module not found" errors
**Problem**: Python dependencies not installed

**Solution**:
```bash
pip install -r requirements.txt
```

### Query returns no results
**Problem**: Question might be ambiguous or data doesn't exist

**Solutions**:
1. Check schema with `schema` command
2. Rephrase your question
3. Be more specific about catalog/schema/table names

## Advanced Usage

### Using with Python Scripts

You can import and use the components in your own scripts:

```python
from dotenv import load_dotenv
from src.config import get_settings
from src.database import DatabaseManager
from src.agent import DatabricksMetadataAgent

# Load environment
load_dotenv()

# Initialize components
settings = get_settings()
db_manager = DatabaseManager(settings)
agent = DatabricksMetadataAgent(settings, db_manager)

# Query
result = agent.query("What tables are in the sales schema?")
print(result["answer"])
```

### Customizing Query Limits

Edit `.env` to change the maximum number of results:
```env
MAX_QUERY_RESULTS=50
```

### Enabling Debug Logging

Set log level in `.env`:
```env
LOG_LEVEL=DEBUG
```

## Data Loading

### Loading Your Own Data

To populate the database with your Databricks metadata:

1. Export your Databricks information_schema tables
2. Transform to match the PostgreSQL schema
3. Load using SQL:

```bash
docker exec -i databricks_metadata_db psql -U dbuser -d databricks_metadata < your_data.sql
```

### Sample Data Structure

The init script provides sample data. To add more:

```sql
-- Connect to database
docker exec -it databricks_metadata_db psql -U dbuser -d databricks_metadata

-- Insert catalog
INSERT INTO catalogs (catalog_name, catalog_owner, comment) 
VALUES ('prod', 'prod_team', 'Production catalog');

-- Insert schema
INSERT INTO schemas (catalog_name, schema_name, schema_owner, comment)
VALUES ('prod', 'finance', 'finance_team', 'Finance data');

-- Insert table
INSERT INTO tables (table_catalog, table_schema, table_name, table_type, table_owner, comment)
VALUES ('prod', 'finance', 'transactions', 'TABLE', 'finance_team', 'Financial transactions');

-- Insert columns
INSERT INTO columns (table_catalog, table_schema, table_name, column_name, ordinal_position, data_type, is_nullable, comment)
VALUES ('prod', 'finance', 'transactions', 'transaction_id', 1, 'BIGINT', false, 'Primary key');
```

## Maintenance

### Viewing Logs

Check application logs:
```bash
python main.py 2>&1 | tee app.log
```

Check database logs:
```bash
docker compose logs -f postgres
```

### Backup Database

Backup the PostgreSQL data:
```bash
docker exec databricks_metadata_db pg_dump -U dbuser databricks_metadata > backup.sql
```

Restore from backup:
```bash
docker exec -i databricks_metadata_db psql -U dbuser -d databricks_metadata < backup.sql
```

### Stopping Services

Stop the database:
```bash
docker compose down
```

Stop and remove data:
```bash
docker compose down -v
```

## Security Best Practices

1. **Never commit `.env` file** - It contains sensitive credentials
2. **Use read-only database user** - Application uses `readonly_user` by default
3. **Keep Azure OpenAI keys secure** - Don't share or expose them
4. **Regularly update dependencies** - Keep packages up to date
5. **Monitor query patterns** - Review logs for unusual activity

## Performance Tips

1. **Index frequently queried columns** - Already done for key columns
2. **Limit result sets** - Use `MAX_QUERY_RESULTS` setting
3. **Batch operations** - Load data in transactions
4. **Monitor database size** - Check `pg_database_size()`

## Getting Help

- Check the main [README.md](README.md) for overview
- Review error messages carefully
- Check Docker and Python logs
- Verify all environment variables are set
- Test components individually with `test_database.py`
