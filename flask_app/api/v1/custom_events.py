from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from schemas.custom_events import CustomEventsSchema
from services.custom_events import CustomEventsService

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('information', location='json', type=dict)
parser.add_argument('time', location='json', type=int, store_missing=False)


class CustomEvents(Resource):
    schema = CustomEventsSchema()
    service = CustomEventsService()

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
            description: Event saved
        """
        user_id = get_jwt_identity()
        args = parser.parse_args()

        self.service.send(user_id, args)

        return '', HTTPStatus.CREATED
