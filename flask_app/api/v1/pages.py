import datetime
from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from api.utils import send_message
from kafka_topics.create_topics import Topics
from schemas.pages import PagesSchema

parser = reqparse.RequestParser()
parser.add_argument('url', location='json')
parser.add_argument('time', location='json', type=int)
parser.add_argument('duration', location='json', type=int)
parser.add_argument('access_token_cookie', location='cookies')


class Pages(Resource):
    schema = PagesSchema()

    @jwt_required()
    def post(self, *args, **kwargs):
        """Endpoint to save page events from user.
        ---
        parameters:
          - name: body
            in: body
            type: string
            required: true
            schema:
              required:
                - url
                - duration
              properties:
                url:
                  type: string
                  description: Request url.
                  default: "string"
                time:
                  type: int
                  description: Time when event happened.
                  default: None
                  example: 1646240200
                duration:
                  type: int
                  description: Duration of page view in seconds.
                  default: None
                  example: 16
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
        send_message(Topics.PAGES, user_event['user_id'], user_event)
        return '', HTTPStatus.CREATED
