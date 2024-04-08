from marshmallow import fields

from schemas.base import BaseSchema


class PagesSchema(BaseSchema):
    url = fields.Str()
    duration = fields.Float()
