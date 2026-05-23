from app.database import engine, Base
# Import all models to ensure they are registered with Base.metadata before calling create_all
from app.models.user import User
from app.models.notice import Notice
from app.models.class_update import ClassUpdate
from app.models.academic import Routine, Assignment, Resource

def setup_tables():
    print("Creating Phase 4 tables (Academic Resource Hub)...")
    # create_all will only create tables that don't already exist
    Base.metadata.create_all(bind=engine)
    print("Setup complete.")

if __name__ == "__main__":
    setup_tables()
