from app.database import engine, Base
from app.models.academic import Routine, Assignment

def setup_phase3():
    print("Creating Phase 3 tables (routines, assignments) if they don't exist...")
    try:
        # Base.metadata.create_all only creates missing tables.
        # We specify the tables to be extra safe.
        Base.metadata.create_all(bind=engine, tables=[Routine.__table__, Assignment.__table__])
        print("Success: Phase 3 tables are ready.")
    except Exception as e:
        print(f"Error creating Phase 3 tables: {e}")

if __name__ == "__main__":
    setup_phase3()
