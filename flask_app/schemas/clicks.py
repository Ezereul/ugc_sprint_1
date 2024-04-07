import datetime

from marshmallow import Schema, fields


class ClickSchema(Schema):
    obj_id = fields.Str()
    user_id = fields.UUID(dump_default=None, load_default=None, allow_none=True)
    time = fields.DateTime(dump_default=datetime.datetime.now())
