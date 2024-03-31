import datetime
from http import HTTPStatus

from flask_restful import Resource, reqparse

from api.utils import send_message
from kafka_topics.create_topics import Topics
from schemas.custom_events import CustomEventsSchema

parser = reqparse.RequestParser()
parser.add_argument('key', location='json')
parser.add_argument('information', location='json', type=dict)
parser.add_argument('time', location='json', type=int)
parser.add_argument('access_token_cookie', location='cookies')


class CustomEvents(Resource):
    schema = CustomEventsSchema()

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
                - key
                - information
              properties:
                key:
                  type: string
                  description: Key of event.
                  default: "string"
                time:
                  type: int
                  description: Time when event happened.
                  default: None
                  example: 1646240200
                information:
                  type: dict
                  description: Custom information.
                  default: None
                  example: {"info": "event description"}
        responses:
          201:
            description: Responses status
        """
        args = parser.parse_args()
        args['time'] = datetime.datetime.fromtimestamp(args['time'])
        user_event = self.schema.dump(args)
        send_message(Topics.CUSTOM_EVENTS, user_event['key'], user_event)
        return '', HTTPStatus.CREATED
