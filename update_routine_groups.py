from app.database import engine, SessionLocal
from sqlalchemy import text, inspect

def migrate():
    print("Starting routine group migration...")
    
    try:
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('routines')]
        
        if "group" not in columns:
            print("Adding 'group' column to routines table...")
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE routines ADD COLUMN \"group\" VARCHAR DEFAULT 'Combined'"))
                conn.commit()
            
            db = SessionLocal()
            print("Updating existing routines to 'Combined' group...")
            db.execute(text("UPDATE routines SET \"group\" = 'Combined' WHERE \"group\" IS NULL"))
            db.commit()
            db.close()
            print("Migration successful.")
        else:
            print("Column 'group' already exists in routines table.")
            
    except Exception as e:
        print("Migration failed:", e)

if __name__ == "__main__":
    migrate()
