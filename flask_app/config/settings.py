from os import environ, path
from pathlib import Path

from dotenv import load_dotenv

basedir = Path(__file__).parent.parent.parent
load_dotenv(path.join(basedir, ".env"))


FLASK_DEBUG = environ.get("FLASK_DEBUG", default=False)
SECRET_KEY = environ.get("SECRET_KEY")

KAFKA_URL = environ.get("KAFKA_URL")
KAFKA_NUM_PARTITIONS = int(environ.get("KAFKA_NUM_PARTITIONS"))
KAFKA_REPLICATION_FACTOR = int(environ.get("KAFKA_REPLICATION_FACTOR"))
KAFKA_RETENTION_MS = environ.get("KAFKA_RETENTION_MS")
KAFKA_MIN_INSYNC_REPLICAS = environ.get("KAFKA_MIN_INSYNC_REPLICAS")

JWT_PUBLIC_KEY = environ.get("JWT_PUBLIC_KEY")
JWT_ALGORITHM = "RS256"
JWT_TOKEN_LOCATION = "cookies"
JWT_COOKIE_CSRF_PROTECT = False
