import datetime

from marshmallow import Schema, fields


class PagesSchema(Schema):
    url = fields.Str()
    user_id = fields.UUID(dump_default=None, load_default=None, allow_none=True)
    duration = fields.Int()
    time = fields.DateTime(dump_default=datetime.datetime.now())
