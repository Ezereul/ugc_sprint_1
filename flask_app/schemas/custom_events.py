import datetime

from marshmallow import Schema, fields


class CustomEventsSchema(Schema):
    key = fields.Str()
    user_id = fields.UUID(dump_default=None, load_default=None, allow_none=True)
    time = fields.DateTime(dump_default=datetime.datetime.now())
    information = fields.Mapping()
