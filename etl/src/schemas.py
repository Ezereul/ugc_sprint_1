import datetime
from typing import Mapping
from uuid import UUID

import msgspec

from src.core.constants import Topics


class BaseEvent(msgspec.Struct, kw_only=True):
    """Каждый Event в системе содержит пользователя, к которому относится и время, когда Event произошёл."""
    user_id: UUID
    time: datetime.datetime


class Click(BaseEvent):
    obj_id: str


class CustomEvent(BaseEvent):
    information: dict


class View(BaseEvent):
    film_id: UUID
    timecode: datetime.time


class Page(BaseEvent):
    url: str
    duration: float


TOPIC_TO_SCHEMA: Mapping[str | Topics, type[msgspec.Struct]] = {
    Topics.CLICKS: Click,
    Topics.CUSTOM_EVENTS: CustomEvent,
    Topics.VIEWS: View,
    Topics.PAGES: Page,
}
