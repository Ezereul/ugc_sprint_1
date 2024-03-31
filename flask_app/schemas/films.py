import datetime

from marshmallow import Schema, fields


class FilmsSchema(Schema):
    film_id = fields.Str()
    user_id = fields.UUID(dump_default=None, load_default=None, allow_none=True)
    timecode = fields.Time(format='%H:%M:%S.%f')
    time = fields.DateTime(dump_default=datetime.datetime.now())
