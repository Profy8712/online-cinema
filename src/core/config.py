from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # General
    DEBUG: bool = False
    TESTING: bool = False

    # Database
    DATABASE_URL: str
    TEST_DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # Auth
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Stripe
    STRIPE_API_KEY: str

    # Email (optional)
    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAIL_FROM: str | None = None

    # Pydantic config
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def db_url(self) -> str:
        """Returns test DB URL if TESTING=True, otherwise main DB URL."""
        return self.TEST_DATABASE_URL if self.TESTING else self.DATABASE_URL


# Global settings instance
settings = Settings()
