import datetime
from typing import Mapping
from uuid import UUID

import msgspec

from src.constants import Topics


class EventMixin:
    user_id: UUID
    time: datetime.datetime


class Click(msgspec.Struct, EventMixin, kw_only=True):
    obj_id: str


class CustomEvent(msgspec.Struct, EventMixin, kw_only=True):
    obj_id: str
    information: dict


class View(msgspec.Struct, EventMixin, kw_only=True):
    film_id: UUID
    timecode: datetime.time


class Page(msgspec.Struct, EventMixin, kw_only=True):
    url: str
    duration: int


TOPIC_TO_SCHEMA: Mapping[str | Topics, type[msgspec.Struct]] = {
    Topics.CLICKS: Click,
    Topics.CUSTOM_EVENTS: CustomEvent,
    Topics.VIEWS: View,
    Topics.PAGES: Page,
}
