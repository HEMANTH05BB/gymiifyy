from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Gamified Fitness Trainer API"
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "gymify"
    enable_db: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
