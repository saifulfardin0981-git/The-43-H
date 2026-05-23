from app.database import engine, SessionLocal
from sqlalchemy import text, inspect

def migrate():
    print("Starting routine course_code migration...")
    
    try:
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('routines')]
        
        if "course_code" not in columns:
            print("Adding 'course_code' column to routines table...")
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE routines ADD COLUMN course_code VARCHAR"))
                conn.commit()
            print("Migration successful.")
        else:
            print("Column 'course_code' already exists in routines table.")
            
    except Exception as e:
        print("Migration failed:", e)

if __name__ == "__main__":
    migrate()
