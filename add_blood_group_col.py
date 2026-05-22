import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Ensure we can import from the app directory to get settings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_migration():
    """
    Bulletproof migration to add 'blood_group' column to the 'users' table.
    Handles reserved keywords and provides detailed error reporting.
    """
    db_url = None
    try:
        # Attempt to load using the application's configuration
        from app.core.config import settings
        db_url = settings.DATABASE_URL
        print(f"Using DATABASE_URL from app settings.")
    except Exception as e:
        print(f"Notice: Could not load app.core.config, falling back to os.getenv: {e}")
        # Manual fallback to environment variable
        db_url = os.getenv("DATABASE_URL")

    if not db_url:
        print("ERROR: DATABASE_URL is not set in .env or environment variables.")
        sys.exit(1)

    # In PostgreSQL, 'user' is a reserved keyword. 
    # Our model defines __tablename__ = "users", but we use double quotes for safety.
    table_name = "users"
    column_name = "blood_group"

    # Fix for newer SQLAlchemy versions that require 'postgresql://' instead of 'postgres://'
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    engine = create_engine(db_url)

    try:
        with engine.connect() as connection:
            print(f"Attempting to add column '{column_name}' to table '\"{table_name}\"'...")
            
            # Use a transaction block
            with connection.begin():
                # SQL command with double-quoted table name to handle reserved keywords/case sensitivity
                sql = text(f'ALTER TABLE "{table_name}" ADD COLUMN {column_name} VARCHAR;')
                connection.execute(sql)
                
            print(f"SUCCESS: Column '{column_name}' added successfully to '{table_name}'.")

    except SQLAlchemyError as e:
        error_msg = str(e)
        # Specifically check if the column already exists
        if "already exists" in error_msg.lower() or "duplicate column" in error_msg.lower():
            print(f"SKIP: Column '{column_name}' already exists in table '{table_name}'.")
        else:
            print("FAILED: A database error occurred during migration:")
            print("-" * 40)
            print(error_msg)
            print("-" * 40)
            sys.exit(1)
    except Exception as e:
        print("CRITICAL: An unexpected system error occurred:")
        print(str(e))
        sys.exit(1)

if __name__ == "__main__":
    run_migration()
