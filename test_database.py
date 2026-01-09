#!/usr/bin/env python3
"""Test script to verify database connectivity and schema."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Settings
from src.database import DatabaseManager


def test_database():
    """Test database connectivity and schema."""
    print("=" * 70)
    print("Testing Database Connectivity")
    print("=" * 70)
    
    # Create settings with default values
    settings = Settings(
        azure_openai_api_key="test-key",
        azure_openai_endpoint="https://test.openai.azure.com/",
        azure_openai_deployment_name="test-deployment",
        postgres_host="localhost",
        postgres_port=5432,
        postgres_db="databricks_metadata",
        postgres_user="readonly_user",
        postgres_password="readonly_pass"
    )
    
    print(f"\n✓ Settings loaded")
    print(f"  Database: {settings.postgres_db}")
    print(f"  Host: {settings.postgres_host}:{settings.postgres_port}")
    
    # Create database manager
    db_manager = DatabaseManager(settings)
    
    # Test connection
    print("\n📡 Testing database connection...")
    if not db_manager.test_connection():
        print("❌ Database connection failed!")
        return False
    
    print("✓ Database connection successful")
    
    # Get table names
    print("\n📋 Retrieving table names...")
    tables = db_manager.get_table_names()
    print(f"✓ Found {len(tables)} tables:")
    for table in tables:
        print(f"  - {table}")
    
    # Test query execution
    print("\n🔍 Testing query execution...")
    try:
        results = db_manager.execute_readonly_query(
            "SELECT COUNT(*) as count FROM catalogs"
        )
        print(f"✓ Query executed successfully")
        print(f"  Catalogs count: {results[0]['count']}")
    except Exception as e:
        print(f"❌ Query execution failed: {e}")
        return False
    
    # Test query with results
    print("\n📊 Retrieving sample data...")
    try:
        results = db_manager.execute_readonly_query(
            "SELECT table_catalog, table_schema, table_name, comment FROM tables LIMIT 5"
        )
        print(f"✓ Retrieved {len(results)} rows")
        for row in results:
            print(f"  - {row['table_catalog']}.{row['table_schema']}.{row['table_name']}")
    except Exception as e:
        print(f"❌ Sample data retrieval failed: {e}")
        return False
    
    # Test safety features
    print("\n🔒 Testing safety features...")
    try:
        db_manager.execute_readonly_query("DELETE FROM catalogs")
        print("❌ Safety check failed - DELETE query was allowed!")
        return False
    except ValueError as e:
        print(f"✓ Safety check passed - dangerous query blocked")
        print(f"  Error: {e}")
    
    # Display schema info
    print("\n📚 Database Schema:")
    print("-" * 70)
    schema_info = db_manager.get_schema_info()
    print(schema_info)
    
    # Cleanup
    db_manager.close()
    
    print("\n" + "=" * 70)
    print("✅ All tests passed successfully!")
    print("=" * 70)
    return True


if __name__ == "__main__":
    try:
        success = test_database()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
