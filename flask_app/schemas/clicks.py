from marshmallow import fields

from schemas.base import BaseSchema


class ClickSchema(BaseSchema):
    obj_id = fields.Str()
