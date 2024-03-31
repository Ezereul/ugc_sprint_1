import datetime

from flask_restful import Resource, reqparse

from api.utils import send_message
from schemas.films import FilmsSchema

parser = reqparse.RequestParser()
parser.add_argument('film_id', location='json')
parser.add_argument('time', location='json', type=int)
parser.add_argument('timecode', location='json')
parser.add_argument('access_token_cookie', location='cookies')


class Films(Resource):
    schema = FilmsSchema()

    def post(self, *args, **kwargs):
        """Endpoint to create a new info from user.
        ---
        parameters:
          - name: body
            in: body
            type: string
            required: true
            schema:
              required:
                - film_id
                - timecode
              properties:
                film_id:
                  type: string
                  description: Film id.
                  default: "string"
                time:
                  type: int
                  description: Time when event happened.
                  default: None
                  example: 1646240200
                timecode:
                  type: int
                  description: Film timecode.
                  default: None
                  example: "03:12:58.019077"
        responses:
          201:
            description: Responses status
        """
        args = parser.parse_args()
        args['time'] = datetime.datetime.fromtimestamp(args['time'])
        args['timecode'] = datetime.datetime.strptime(args['timecode'], '%H:%M:%S.%f')
        user_event = self.schema.dump(args)
        send_message('views', user_event['film_id'], user_event)
        return '', 201
