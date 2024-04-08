from kafka_topics.create import Topics
from schemas.clicks import ClickSchema
from services.base import BaseService


class ClicksService(BaseService):
    schema = ClickSchema()
    topic = Topics.CLICKS
