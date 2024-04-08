from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from schemas.clicks import ClickSchema
from services.clicks import ClicksService

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('obj_id', location='json')
parser.add_argument('time', location='json', type=int, store_missing=False)


class Clicks(Resource):
    schema = ClickSchema()
    service = ClicksService()

    @jwt_required()
    def post(self, *args, **kwargs):
        """Endpoint to save click events from user.
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
                  default: None
                  example: "string"
                time:
                  type: int
                  description: Timestamp when event happened.
                  default: None
                  example: 1646240200
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
