from os import environ, path
from pathlib import Path

from dotenv import load_dotenv

# a = path.dirname(__file__)
# basedir = path.abspath(path.dirname(__file__))

basedir = Path(__file__).parent.parent.parent
load_dotenv(path.join(basedir, ".env"))


# ENVIRONMENT = environ.get("ENVIRONMENT")
# FLASK_APP = environ.get("FLASK_APP")
FLASK_DEBUG = environ.get("FLASK_DEBUG")
SECRET_KEY = environ.get("SECRET_KEY")

KAFKA_URL = environ.get("KAFKA_URL")
a = 1