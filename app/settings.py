from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_password: str = "postgres"
    postgres_db: str = "postgres"
    postgres_user: str = "postgres"
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    secret_key: str = "secret_key"

    def db_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
