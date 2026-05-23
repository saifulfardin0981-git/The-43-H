from app.database import engine, SessionLocal, Base
from app.models.academic import Semester, Course, Resource
from sqlalchemy import text, inspect

def migrate():
    print("Starting Nested Resource Hub migration...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        inspector = inspect(engine)
        
        # 1. Add category and course_id to resources
        columns = [col['name'] for col in inspector.get_columns('resources')]
        
        with engine.connect() as conn:
            if "category" not in columns:
                print("Adding 'category' column to resources table...")
                conn.execute(text("ALTER TABLE resources ADD COLUMN category VARCHAR DEFAULT 'Other'"))
            
            if "course_id" not in columns:
                print("Adding 'course_id' column to resources table...")
                conn.execute(text("ALTER TABLE resources ADD COLUMN course_id INTEGER REFERENCES courses(id)"))
            
            conn.commit()

        # 2. Cleanup (Optional: remove subject if it exists and we're sure)
        # Note: Removing columns in SQLite/Postgres via raw SQL ALTER is sometimes complex, 
        # so we'll leave it for now to avoid data loss during the transition.
        
        print("Migration successful.")
            
    except Exception as e:
        print("Migration failed:", e)
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
