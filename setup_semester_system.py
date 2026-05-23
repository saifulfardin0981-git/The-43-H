from app.database import engine, SessionLocal, Base
from app.models.academic import Semester, Resource
from sqlalchemy import text, inspect

def setup():
    print("Setting up Semester System...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Create default semester if none exists
    if not db.query(Semester).first():
        sem = Semester(code="262", name="Summer 2026", is_current=True)
        db.add(sem)
        db.commit()
        db.refresh(sem)
        print(f"Created default semester: {sem.name}")
    
    # Update existing resources to the current semester if they have no semester_id
    try:
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('resources')]
        
        if "semester_id" not in columns:
            print("Adding semester_id column to resources table...")
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE resources ADD COLUMN semester_id INTEGER REFERENCES semesters(id)"))
                conn.commit()
                
        current_sem = db.query(Semester).filter(Semester.is_current == True).first()
        if current_sem:
            print("Associating existing resources with current semester...")
            db.execute(text(f"UPDATE resources SET semester_id = {current_sem.id} WHERE semester_id IS NULL"))
            db.commit()
    except Exception as e:
        print("Migration error or already migrated:", e)
        
    db.close()
    print("Semester setup complete.")

if __name__ == "__main__":
    setup()
