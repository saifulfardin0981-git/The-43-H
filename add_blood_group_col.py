from sqlalchemy import text
from app.database import engine

def add_blood_group_column():
    with engine.connect() as conn:
        print("Checking if 'blood_group' column exists...")
        result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name='blood_group';"))
        if not result.fetchone():
            print("Adding 'blood_group' column to 'users' table...")
            conn.execute(text("ALTER TABLE users ADD COLUMN blood_group VARCHAR;"))
            conn.commit()
            print("Column added successfully.")
        else:
            print("Column 'blood_group' already exists.")

if __name__ == "__main__":
    add_blood_group_column()
