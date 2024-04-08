from kafka_topics.create import Topics
from schemas.films import FilmsSchema
from services.base import BaseService


class FilmsService(BaseService):
    schema = FilmsSchema()
    topic = Topics.VIEWS
