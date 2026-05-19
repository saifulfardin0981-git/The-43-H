import sys
import os

# Add the project root to sys.path so we can import from 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User

def setup_role():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        print("--- Update User to Absolute Admin (Role 4) ---")
        email = input("Enter User Email: ")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"Error: User with email '{email}' not found. They must login once first.")
            return

        user.role = 4
        db.commit()
        print(f"Successfully updated {user.name} ({user.email}) to Role 4 (Absolute Admin).")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_role()
