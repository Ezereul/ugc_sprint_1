from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent.parent
ENV_PATH = PROJECT_ROOT / '.env'


class ETLSettings(BaseSettings):
    kafka_url: str
    consumer_timeout_ms: int
    consumer_min_poll_records: int
    log_level: str
    log_format: str

    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore')


settings = ETLSettings()
