import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ENV_PATH = PROJECT_ROOT / '.env'


class ETLSettings(BaseSettings):
    kafka_url: str
    consumer_timeout_ms: int
    consumer_min_poll_records: int
    log_level: str
    log_format: str
    clickhouse_1_host: str
    clickhouse_2_host: str
    clickhouse_3_host: str
    clickhouse_4_host: str
    clickhouse_1_port: int
    clickhouse_2_port: int
    clickhouse_3_port: int
    clickhouse_4_port: int

    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore')


settings = ETLSettings()

logger = logging.getLogger(__name__)
logging.basicConfig(format=settings.log_format, level=settings.log_level)
