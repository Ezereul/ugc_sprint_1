import datetime
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from flask_app.api.utils import send_message
from flask_app.kafka_topics.create_topics import Topics
from flask_app.schemas.custom_events import CustomEventsSchema

parser = reqparse.RequestParser()
parser.add_argument('information', location='json', type=dict)
parser.add_argument('time', location='json', type=int)


class CustomEvents(Resource):
    schema = CustomEventsSchema()

    @jwt_required()
    def post(self, *args, **kwargs):
        """Endpoint to save some custom events from user.
        ---
        parameters:
          - name: body
            in: body
            type: string
            required: true
            schema:
              required:
                - information
              properties:
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
        security:
          - cookieAuth: []
        responses:
          201:
            description: Responses status
        """
        user_id = get_jwt_identity()
        args = parser.parse_args()
        args['time'] = datetime.datetime.fromtimestamp(args['time'])
        args['user_id'] = user_id
        user_event = self.schema.dump(args)
        send_message(Topics.CUSTOM_EVENTS, user_event['user_id'], user_event)
        return '', HTTPStatus.CREATED
