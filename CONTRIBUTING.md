# Contributing Guide

Thank you for your interest in contributing to the Databricks Metadata Chat Assistant!

## Development Setup

1. Fork and clone the repository
2. Set up your development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Start the database:
   ```bash
   docker compose up -d
   ```

4. Run tests:
   ```bash
   python test_database.py
   ```

## Project Structure

```
.
├── src/
│   ├── __init__.py         # Package initialization
│   ├── agent.py            # LangChain SQL agent
│   ├── cli.py              # Interactive CLI interface
│   ├── config.py           # Configuration management
│   └── database.py         # Database operations
├── sql/
│   └── init.sql            # Database schema and sample data
├── main.py                 # Application entry point
├── test_database.py        # Database tests
└── docker-compose.yml      # PostgreSQL setup
```

## Making Changes

### Adding New Features

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the coding standards below

3. Test your changes thoroughly

4. Commit with descriptive messages:
   ```bash
   git commit -m "Add feature: description"
   ```

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings for functions and classes
- Keep functions focused and modular
- Add comments for complex logic

### Testing

Before submitting changes:

1. **Test database connectivity:**
   ```bash
   python test_database.py
   ```

2. **Test the CLI manually:**
   ```bash
   python main.py
   ```
   Try various queries to ensure functionality

3. **Check for syntax errors:**
   ```bash
   python -m py_compile src/*.py
   ```

## Enhancement Ideas

### High Priority
- Add unit tests for individual components
- Implement query history and favorites
- Add support for exporting results (CSV, JSON)
- Implement query result caching

### Medium Priority
- Add support for more complex queries (JOINs, aggregations)
- Create a web interface (optional, currently CLI-only)
- Add support for custom data sources
- Implement query performance monitoring

### Low Priority
- Add support for multiple Azure OpenAI deployments
- Implement query templates
- Add natural language response improvements
- Create a plugin system for extensions

## Areas for Contribution

### Documentation
- Improve README with more examples
- Add troubleshooting guides
- Create video tutorials
- Translate documentation

### Features
- Enhance SQL agent prompts
- Add more database schema support
- Improve error handling
- Add query validation improvements

### Testing
- Add unit tests
- Add integration tests
- Add performance tests
- Add security tests

### Infrastructure
- CI/CD pipeline setup
- Docker image optimization
- Kubernetes deployment configs
- Monitoring and logging improvements

## Pull Request Process

1. **Before submitting:**
   - Test all changes locally
   - Update documentation if needed
   - Add comments to complex code
   - Ensure no security vulnerabilities

2. **Submit PR with:**
   - Clear title describing the change
   - Description of what changed and why
   - Screenshots for UI changes (if applicable)
   - Test results or validation steps

3. **PR Review:**
   - Address reviewer feedback
   - Keep commits organized
   - Squash commits if requested

## Security Guidelines

### Critical
- Never commit API keys or secrets
- Always use parameterized queries
- Validate all user inputs
- Follow the principle of least privilege

### Best Practices
- Use the read-only database user by default
- Implement proper error handling
- Log security-relevant events
- Keep dependencies updated

## Database Changes

If modifying the database schema:

1. Update `sql/init.sql`
2. Update sample data
3. Update documentation
4. Test migration path
5. Document breaking changes

Example:
```sql
-- Add new column
ALTER TABLE tables ADD COLUMN created_by VARCHAR(255);

-- Update sample data
UPDATE tables SET created_by = 'system' WHERE created_by IS NULL;
```

## LangChain Agent Changes

When modifying the agent:

1. **Test thoroughly** - AI behavior can be unpredictable
2. **Monitor token usage** - Keep costs reasonable
3. **Validate safety** - Ensure queries remain read-only
4. **Document changes** - Explain prompt modifications

Example prompt improvement:
```python
context = """You are an expert SQL assistant...
New instruction: When showing results, always include the source table.
"""
```

## Common Issues

### Issue: "Module not found"
**Solution:** Ensure virtual environment is activated and dependencies installed

### Issue: Database connection fails
**Solution:** Check Docker is running and PostgreSQL is healthy

### Issue: Azure OpenAI errors
**Solution:** Verify API credentials and rate limits

## Getting Help

- Check existing documentation (README.md, USAGE.md)
- Review code comments and docstrings
- Look at existing implementations for patterns
- Open an issue for discussion before major changes

## Code Review Checklist

Before submitting, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
- [ ] Error handling is appropriate
- [ ] Logging is adequate
- [ ] Comments explain complex logic
- [ ] Type hints are used
- [ ] Code is DRY (Don't Repeat Yourself)
- [ ] Performance is acceptable

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Questions?

Feel free to open an issue for:
- Feature discussions
- Implementation questions
- Bug reports
- General questions

Thank you for contributing! 🎉
