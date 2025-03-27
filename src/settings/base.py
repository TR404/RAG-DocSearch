from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='./.env', extra='ignore')

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    OPENAI_API_KEY: str
    OPENAI_ORGANIZATION_ID: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def database_url(self) -> str:
        """Generate PostgreSQL connection URL"""
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

settings = Settings()
