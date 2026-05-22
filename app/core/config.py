from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "43-H API"
    # To run locally with SQLite as fallback, but designed for Postgres
    DATABASE_URL: str = "sqlite:///./test.db" 
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" # Example key, change in prod
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google OAuth2 Settings
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    SECRET_KEY_SESSION: str = "your-session-secret-key" # Used for SessionMiddleware

    class Config:
        env_file = ".env"

settings = Settings()
