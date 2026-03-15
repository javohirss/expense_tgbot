from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    BASE_URL: str
    DB_URI: str
    DB_URL: str
    GEMINI_API_KEY: str


    class Config:
        env_file = ".env"


settings = Settings()