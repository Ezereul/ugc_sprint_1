from marshmallow import fields

from schemas.base import BaseSchema


class CustomEventsSchema(BaseSchema):
    information = fields.Mapping()
