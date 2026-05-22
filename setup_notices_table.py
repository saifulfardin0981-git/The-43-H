from app.database import engine, Base
from app.models.notice import Notice

def setup_notices():
    print("Creating 'notices' table if it doesn't exist...")
    try:
        # This will only create tables that do not already exist in the database.
        # Since we've imported Notice, it's included in Base.metadata.
        Base.metadata.create_all(bind=engine, tables=[Notice.__table__])
        print("Success: 'notices' table is ready.")
    except Exception as e:
        print(f"Error creating 'notices' table: {e}")

if __name__ == "__main__":
    setup_notices()
