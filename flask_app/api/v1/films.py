from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from flask_app.schemas.films import FilmsSchema
from flask_app.services.films import FilmsService

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('film_id', location='json')
parser.add_argument('time', location='json', type=int, store_missing=False)
parser.add_argument('timecode', location='json')


class Films(Resource):
    service = FilmsService()
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
            description: Event saved
        """
        user_id = get_jwt_identity()
        args = parser.parse_args()

        self.service.send(user_id, args)

        return '', HTTPStatus.CREATED
