from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent
ENV_FILEPATH = Path(BASE_DIR / ".env")


class _Settings(BaseSettings):
    FLASK_DEBUG: bool = False
    SECRET_KEY: str

    KAFKA_URL: str
    KAFKA_NUM_PARTITIONS: int
    KAFKA_REPLICATION_FACTOR: int
    KAFKA_RETENTION_MS: str
    KAFKA_MIN_INSYNC_REPLICAS: str

    JWT_PUBLIC_KEY: str
    JWT_ALGORITHM: str = "RS256"
    JWT_TOKEN_LOCATION: str = "cookies"
    JWT_COOKIE_CSRF_PROTECT: bool = False

    model_config = SettingsConfigDict(env_file=ENV_FILEPATH, extra="ignore")


settings = _Settings()
