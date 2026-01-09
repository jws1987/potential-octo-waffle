# Quick Reference

## Starting Up

```bash
# 1. Start database
docker compose up -d

# 2. Run the assistant
python main.py
```

## Essential Commands

| Command | Description |
|---------|-------------|
| `schema` | Show complete database schema |
| `help` | Display help information |
| `quit` or `exit` | Exit the application |

## Common Queries

### Catalogs
```
List all catalogs
Show catalogs with their owners
How many catalogs exist?
```

### Schemas  
```
What schemas are in the main catalog?
Show all schemas owned by sales_team
List schemas with their comments
```

### Tables
```
What tables are in main.sales?
Show all tables in the customer schema
List VIEW type tables
Which tables are owned by analytics_team?
```

### Columns
```
What columns are in the orders table?
Show data types for customers table columns
Which columns allow NULL values in products?
List all BIGINT columns
```

### Complex Queries
```
Find tables related to customers
Show tables with column counts
List all foreign key relationships
Which tables have comments?
```

## Troubleshooting

### Database Won't Start
```bash
docker compose down
docker compose up -d
docker compose ps
```

### Connection Failed
```bash
# Test connection
python test_database.py

# Check logs
docker compose logs postgres
```

### Azure OpenAI Error
- Verify credentials in `.env`
- Check API key is valid
- Confirm endpoint URL format
- Test in Azure Portal

## File Locations

| File | Purpose |
|------|---------|
| `.env` | Configuration (API keys, DB settings) |
| `main.py` | Run the application |
| `test_database.py` | Test database connectivity |
| `setup.sh` | Automated setup script |
| `README.md` | Full documentation |
| `USAGE.md` | Detailed usage guide |

## Database Info

**Schema:** catalogs → schemas → tables → columns  
**Port:** 5432 (localhost)  
**Database:** databricks_metadata  
**User:** readonly_user (read-only access)

## Safety Features

✅ Read-only queries only  
✅ Query validation (blocks DML/DDL)  
✅ Result limits (100 rows default)  
✅ Dedicated read-only database user  
✅ Connection pooling disabled (CLI usage)

## Tips

1. Be specific in your questions
2. Use table/schema names when known
3. Ask follow-up questions to refine results
4. Use `schema` command to explore structure
5. Check logs if queries fail

## Environment Variables

Required:
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT_NAME`

Optional:
- `MAX_QUERY_RESULTS` (default: 100)
- `LOG_LEVEL` (default: INFO)

## Next Steps

1. ✅ Review [README.md](README.md) for setup
2. ✅ Check [USAGE.md](USAGE.md) for examples
3. ✅ Run `setup.sh` for automated setup
4. ✅ Test with `test_database.py`
5. ✅ Start chatting with `python main.py`
