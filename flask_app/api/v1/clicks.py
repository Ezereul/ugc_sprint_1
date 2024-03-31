import datetime
from http import HTTPStatus

from flask_restful import Resource, reqparse

from api.utils import send_message
from kafka_topics.create_topics import Topics
from schemas.clicks import ClickSchema

parser = reqparse.RequestParser()
parser.add_argument('obj_id', location='json')
parser.add_argument('time', location='json', type=int)
parser.add_argument('access_token_cookie', location='cookies')


class Clicks(Resource):
    schema = ClickSchema()

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
                - obj_id
              properties:
                obj_id:
                  type: string
                  description: Object id.
                  default: "string"
                time:
                  type: int
                  description: Time when event happened.
                  default: None
                  example: 1646240200
        responses:
          201:
            description: Responses status
        """
        args = parser.parse_args()
        args['time'] = datetime.datetime.fromtimestamp(args['time'])
        user_click = self.schema.dump(args)
        send_message(Topics.CLICKS, user_click['obj_id'], user_click)

        return '', HTTPStatus.CREATED
