from marshmallow import fields

from schemas.base import BaseSchema


class FilmsSchema(BaseSchema):
    film_id = fields.Str()
    timecode = fields.Time(format='%H:%M:%S.%f')
