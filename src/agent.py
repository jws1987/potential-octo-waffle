"""LangChain-based chat agent for Databricks metadata queries."""

from langchain_openai import AzureChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.schema import AgentAction, AgentFinish
from typing import Optional, Dict, Any
import logging

from .config import Settings
from .database import DatabaseManager

logger = logging.getLogger(__name__)


class DatabricksMetadataAgent:
    """
    LangChain-based agent for querying Databricks metadata.
    
    This agent uses Azure OpenAI and LangChain's SQL agent to convert
    natural language queries into SQL and execute them safely.
    """
    
    def __init__(self, settings: Settings, db_manager: DatabaseManager):
        """Initialize the agent with settings and database manager."""
        self.settings = settings
        self.db_manager = db_manager
        self._agent = None
        self._llm = None
    
    @property
    def llm(self) -> AzureChatOpenAI:
        """Lazy-load Azure OpenAI LLM."""
        if self._llm is None:
            self._llm = AzureChatOpenAI(
                azure_endpoint=self.settings.azure_openai_endpoint,
                azure_deployment=self.settings.azure_openai_deployment_name,
                api_version=self.settings.azure_openai_api_version,
                api_key=self.settings.azure_openai_api_key,
                temperature=0,  # Deterministic for SQL generation
                max_tokens=1500
            )
            logger.info("Azure OpenAI LLM initialized")
        return self._llm
    
    @property
    def agent(self):
        """Lazy-load SQL agent."""
        if self._agent is None:
            # Create SQLDatabase wrapper
            db = SQLDatabase(self.db_manager.engine)
            
            # Create toolkit
            toolkit = SQLDatabaseToolkit(db=db, llm=self.llm)
            
            # Create agent with custom prompt
            self._agent = create_sql_agent(
                llm=self.llm,
                toolkit=toolkit,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                max_iterations=10,
                max_execution_time=60,
                handle_parsing_errors=True,
                agent_executor_kwargs={
                    "return_intermediate_steps": True
                }
            )
            logger.info("SQL agent created")
        return self._agent
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Process a natural language question about Databricks metadata.
        
        Args:
            question: Natural language question
            
        Returns:
            Dictionary containing the answer and additional metadata
        """
        try:
            logger.info(f"Processing question: {question}")
            
            # Add context to the question
            context = self._build_context()
            full_question = f"{context}\n\nQuestion: {question}"
            
            # Execute agent
            result = self.agent.invoke({"input": full_question})
            
            return {
                "question": question,
                "answer": result.get("output", "No answer generated"),
                "success": True,
                "intermediate_steps": result.get("intermediate_steps", [])
            }
        
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return {
                "question": question,
                "answer": f"Error: {str(e)}",
                "success": False,
                "error": str(e)
            }
    
    def _build_context(self) -> str:
        """Build context string for the agent."""
        context = """You are an expert SQL assistant helping users query Databricks metadata.

The database contains the following tables that mirror Databricks information_schema:

1. **catalogs**: Contains catalog information
   - catalog_name, catalog_owner, comment, created_at

2. **schemas**: Contains schema information  
   - catalog_name, schema_name, schema_owner, comment, created_at

3. **tables**: Contains table information
   - table_catalog, table_schema, table_name, table_type, table_owner, comment, created_at

4. **columns**: Contains column information
   - table_catalog, table_schema, table_name, column_name, ordinal_position, 
     data_type, is_nullable, column_default, comment

Important guidelines:
- Only generate SELECT queries (read-only)
- Use proper JOIN conditions when querying across tables
- Filter results appropriately to answer the specific question
- Provide clear, concise answers based on the query results
- If no data is found, clearly state that
"""
        return context
    
    def get_schema_summary(self) -> str:
        """Get a summary of the database schema."""
        return self.db_manager.get_schema_info()
