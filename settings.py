from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Tusdatos API MVP"
    env: str
    secret_key: str
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"
