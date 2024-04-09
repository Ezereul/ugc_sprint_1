from kafka_topics.create import Topics
from schemas.pages import PagesSchema
from services.base import BaseService


class PagesService(BaseService):
    schema = PagesSchema()
    topic = Topics.PAGES
