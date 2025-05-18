import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "Ecommerce Service"
    PROJECT_VERSION: str = "0.0.1"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Database settings
    DB_USER: str = os.getenv("USER_DB_USER", "ranecs")
    DB_PASSWORD: str = os.getenv("USER_DB_PASSWORD", "ranecs")
    DB_NAME: str = os.getenv("USER_DB_NAME", "gencode")
    DB_HOST: str = os.getenv("USER_DB_HOST", "localhost")
    DB_PORT: str = os.getenv("USER_DB_PORT", "5432")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "defaultsecretkey")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 200)
    )
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

    # Construct the database URL
    DB_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    class Config:
        # env_file = env_file_path
        extra = "allow"


settings = Settings()
