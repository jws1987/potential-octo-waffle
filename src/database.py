"""Database connection and management utilities."""

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.pool import NullPool
from typing import List, Dict, Any
import logging

from .config import Settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and provides safe query execution."""
    
    def __init__(self, settings: Settings):
        """Initialize database manager with settings."""
        self.settings = settings
        self._engine: Engine = None
    
    @property
    def engine(self) -> Engine:
        """Lazy-load database engine."""
        if self._engine is None:
            self._engine = create_engine(
                self.settings.database_url,
                poolclass=NullPool,  # No connection pooling for CLI app
                echo=False
            )
            logger.info("Database engine created")
        return self._engine
    
    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                result.fetchone()
            logger.info("Database connection successful")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def get_table_names(self) -> List[str]:
        """Get all table names in the database."""
        inspector = inspect(self.engine)
        return inspector.get_table_names()
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific table."""
        inspector = inspect(self.engine)
        columns = inspector.get_columns(table_name)
        primary_keys = inspector.get_pk_constraint(table_name)
        
        return {
            "table_name": table_name,
            "columns": columns,
            "primary_keys": primary_keys.get("constrained_columns", [])
        }
    
    def execute_readonly_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a read-only query safely.
        
        Args:
            query: SQL query to execute
            
        Returns:
            List of dictionaries representing query results
            
        Raises:
            ValueError: If query contains forbidden keywords
        """
        # Safety check: ensure query is read-only
        forbidden_keywords = [
            "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", 
            "ALTER", "TRUNCATE", "GRANT", "REVOKE"
        ]
        
        query_upper = query.upper()
        for keyword in forbidden_keywords:
            if keyword in query_upper:
                raise ValueError(f"Query contains forbidden keyword: {keyword}")
        
        # Execute query with limit
        limited_query = query
        if "LIMIT" not in query_upper:
            limited_query = f"{query.rstrip(';')} LIMIT {self.settings.max_query_results}"
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(limited_query))
                # Convert rows to dictionaries
                rows = [dict(row._mapping) for row in result]
                logger.info(f"Query executed successfully, returned {len(rows)} rows")
                return rows
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def get_schema_info(self) -> str:
        """
        Get a formatted string with schema information for LLM context.
        
        Returns:
            Formatted schema information
        """
        schema_info = []
        schema_info.append("Database Schema Information:")
        schema_info.append("=" * 80)
        
        for table_name in self.get_table_names():
            table_info = self.get_table_info(table_name)
            schema_info.append(f"\nTable: {table_name}")
            schema_info.append("-" * 40)
            
            for col in table_info["columns"]:
                pk_marker = " [PK]" if col["name"] in table_info["primary_keys"] else ""
                nullable = "NULL" if col["nullable"] else "NOT NULL"
                schema_info.append(
                    f"  - {col['name']}: {col['type']} {nullable}{pk_marker}"
                )
        
        return "\n".join(schema_info)
    
    def close(self):
        """Close database connections."""
        if self._engine is not None:
            self._engine.dispose()
            logger.info("Database connections closed")
