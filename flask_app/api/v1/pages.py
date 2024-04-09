from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from flask_app.schemas.pages import PagesSchema
from flask_app.services.pages import PagesService

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('url', location='json')
parser.add_argument('time', location='json', type=int, store_missing=False)
parser.add_argument('duration', location='json', type=int)


class Pages(Resource):
    schema = PagesSchema()
    service = PagesService()

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
                  type: float
                  description: Duration of page view in seconds.
                  default: None
                  example: 14.1
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
