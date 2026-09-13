from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TaskFlow API"
    database_url: str = "sqlite:///./taskflow.db"
    secret_key: str = "local-development-secret-change-me"
    access_token_expire_minutes: int = 60 * 24
    frontend_url: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
