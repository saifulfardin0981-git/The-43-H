from app.database import engine, SessionLocal, Base
from app.models.site_settings import SiteSettings
from app.models.user import User
from sqlalchemy import text, inspect

def setup():
    print("Setting up Ad Management System...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Create global settings if none exist
        if not db.query(SiteSettings).first():
            settings = SiteSettings(global_ads_enabled=True)
            db.add(settings)
            db.commit()
            print("Created default SiteSettings.")

        # Check and add ads_enabled column to users
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('users')]
        
        if "ads_enabled" not in columns:
            print("Adding ads_enabled column to users table...")
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN ads_enabled BOOLEAN DEFAULT true"))
                conn.commit()
                
            print("Updating existing users to have ads enabled...")
            db.execute(text("UPDATE users SET ads_enabled = true WHERE ads_enabled IS NULL"))
            db.commit()
        else:
            print("ads_enabled column already exists in users table.")
            
    except Exception as e:
        print("Migration error:", e)
        
    db.close()
    print("Ad Management setup complete.")

if __name__ == "__main__":
    setup()
