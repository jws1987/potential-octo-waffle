"""Command-line interface for the Databricks Metadata Chat Assistant."""

import sys
import logging
from typing import Optional
from dotenv import load_dotenv

from .config import get_settings
from .database import DatabaseManager
from .agent import DatabricksMetadataAgent


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChatCLI:
    """Command-line interface for the chat assistant."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.settings = None
        self.db_manager = None
        self.agent = None
    
    def initialize(self) -> bool:
        """
        Initialize all components.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Load environment variables
            load_dotenv()
            
            # Load settings
            logger.info("Loading configuration...")
            self.settings = get_settings()
            
            # Initialize database manager
            logger.info("Initializing database connection...")
            self.db_manager = DatabaseManager(self.settings)
            
            # Test database connection
            if not self.db_manager.test_connection():
                logger.error("Failed to connect to database")
                return False
            
            # Initialize agent
            logger.info("Initializing AI agent...")
            self.agent = DatabricksMetadataAgent(self.settings, self.db_manager)
            
            logger.info("Initialization complete")
            return True
            
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            return False
    
    def print_banner(self):
        """Print welcome banner."""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║   Databricks Metadata Chat Assistant                        ║
║   Powered by LangChain & Azure OpenAI                        ║
╚══════════════════════════════════════════════════════════════╝

Ask questions about your Databricks catalog, tables, columns, and metadata.

Commands:
  - Type your question naturally
  - 'schema' - Show database schema
  - 'help' - Show this help message
  - 'quit' or 'exit' - Exit the application

Examples:
  - "What tables are in the sales schema?"
  - "Show me all columns in the orders table"
  - "List all catalogs and their owners"
  - "Which tables contain customer information?"

"""
        print(banner)
    
    def print_help(self):
        """Print help message."""
        help_text = """
Available Commands:
  schema      - Display the complete database schema
  help        - Show this help message
  quit/exit   - Exit the application

You can ask questions like:
  - "What tables exist in the main catalog?"
  - "Show me columns in the customers table"
  - "Which schemas are owned by the sales team?"
  - "List all tables with their descriptions"
  - "What data types are used in the products table?"
"""
        print(help_text)
    
    def handle_command(self, user_input: str) -> bool:
        """
        Handle special commands.
        
        Args:
            user_input: User input string
            
        Returns:
            True if command was handled, False otherwise
        """
        command = user_input.lower().strip()
        
        if command in ['quit', 'exit']:
            print("\nThank you for using Databricks Metadata Chat Assistant!")
            return True
        
        elif command == 'help':
            self.print_help()
            return True
        
        elif command == 'schema':
            print("\n" + self.agent.get_schema_summary())
            return True
        
        return False
    
    def process_question(self, question: str):
        """
        Process a user question.
        
        Args:
            question: User's question
        """
        print("\n🤔 Thinking...")
        
        result = self.agent.query(question)
        
        print("\n" + "=" * 70)
        if result["success"]:
            print(f"📊 Answer:\n{result['answer']}")
        else:
            print(f"❌ Error: {result['answer']}")
        print("=" * 70 + "\n")
    
    def run(self):
        """Run the interactive CLI."""
        # Initialize
        if not self.initialize():
            print("❌ Failed to initialize. Please check your configuration.")
            print("Make sure:")
            print("  1. PostgreSQL is running (docker-compose up -d)")
            print("  2. .env file exists with Azure OpenAI credentials")
            sys.exit(1)
        
        # Print banner
        self.print_banner()
        
        # Main loop
        try:
            while True:
                try:
                    user_input = input("\n💬 You: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Handle special commands
                    if self.handle_command(user_input):
                        if user_input.lower() in ['quit', 'exit']:
                            break
                        continue
                    
                    # Process question
                    self.process_question(user_input)
                
                except KeyboardInterrupt:
                    print("\n\nInterrupted by user.")
                    break
                except EOFError:
                    print("\n\nEnd of input.")
                    break
        
        finally:
            # Cleanup
            if self.db_manager:
                self.db_manager.close()
            print("\nGoodbye! 👋")


def main():
    """Main entry point."""
    cli = ChatCLI()
    cli.run()


if __name__ == "__main__":
    main()
