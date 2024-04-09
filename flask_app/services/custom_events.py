from kafka_topics.create import Topics
from schemas.custom_events import CustomEventsSchema
from services.base import BaseService


class CustomEventsService(BaseService):
    schema = CustomEventsSchema()
    topic = Topics.CUSTOM_EVENTS
