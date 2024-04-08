from marshmallow import Schema, fields

from utils.datetimes import datetime_now


class BaseSchema(Schema):
    user_id = fields.UUID(required=True)
    time = fields.DateTime('timestamp', load_default=datetime_now)
