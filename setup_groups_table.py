from app.database import engine, Base
# Import models to ensure they are registered
from app.models.user import User
from app.models.notice import Notice
from app.models.class_update import ClassUpdate
from app.models.academic import Routine, Assignment, Resource, Semester, Course, GroupLink

def setup_groups():
    print("Initializing Group Links table...")
    # This will safely create only the group_links table if others exist
    Base.metadata.create_all(bind=engine)
    print("Setup complete. group_links table is ready.")

if __name__ == "__main__":
    setup_groups()
