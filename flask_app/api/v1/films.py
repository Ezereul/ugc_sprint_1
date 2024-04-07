import datetime
from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from api.utils import send_message
from kafka_topics.create_topics import Topics
from schemas.films import FilmsSchema

parser = reqparse.RequestParser()
parser.add_argument('film_id', location='json')
parser.add_argument('time', location='json', type=int)
parser.add_argument('timecode', location='json')


class Films(Resource):
    schema = FilmsSchema()

    @jwt_required()
    def post(self, *args, **kwargs):
        """Endpoint to save a new events from user about films.
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
                  default: None
                  example: "ccc94e57-a383-450b-a1e2-7be0a2786fa2"
                time:
                  type: int
                  description: Time when event happened.
                  default: None
                  example: 1646240200
                timecode:
                  type: str
                  description: Film timecode.
                  default: None
                  example: "03:12:58.019077"
        security:
          - cookieAuth: []
        responses:
          201:
            description: Responses status
        """
        user_id = get_jwt_identity()
        args = parser.parse_args()
        args['time'] = datetime.datetime.fromtimestamp(args['time'])
        args['timecode'] = datetime.datetime.strptime(args['timecode'], '%H:%M:%S.%f')
        args['user_id'] = user_id
        user_event = self.schema.dump(args)
        send_message(Topics.VIEWS, user_event['user_id'], user_event)
        return '', HTTPStatus.CREATED
