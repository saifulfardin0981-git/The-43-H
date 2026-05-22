import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Ensure we can import from the app directory to get settings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_migration():
    """
    Migration to add 'resources_link' column to the 'notices' table.
    """
    db_url = None
    try:
        from app.core.config import settings
        db_url = settings.DATABASE_URL
        print(f"Using DATABASE_URL from app settings.")
    except Exception as e:
        print(f"Notice: Falling back to os.getenv: {e}")
        db_url = os.getenv("DATABASE_URL")

    if not db_url:
        print("ERROR: DATABASE_URL is not set.")
        sys.exit(1)

    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    engine = create_engine(db_url)

    try:
        with engine.connect() as connection:
            print("Attempting to add column 'resources_link' to table 'notices'...")
            with connection.begin():
                # SQL command to add the column
                sql = text('ALTER TABLE notices ADD COLUMN resources_link VARCHAR;')
                connection.execute(sql)
            print("SUCCESS: Column 'resources_link' added successfully.")

    except SQLAlchemyError as e:
        error_msg = str(e)
        if "already exists" in error_msg.lower() or "duplicate column" in error_msg.lower():
            print("SKIP: Column 'resources_link' already exists.")
        else:
            print("FAILED: A database error occurred during migration:")
            print("-" * 40)
            print(error_msg)
            print("-" * 40)
            sys.exit(1)
    except Exception as e:
        print(f"CRITICAL Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migration()
