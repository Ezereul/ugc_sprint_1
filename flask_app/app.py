from http import HTTPStatus

import orjson
from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from kafka import KafkaProducer
from marshmallow import ValidationError

from flask_app.api.v1.clicks import Clicks
from flask_app.api.v1.custom_events import CustomEvents
from flask_app.api.v1.films import Films
from flask_app.api.v1.pages import Pages
from flask_app.kafka_topics.create_topics import create_topics
from flask_app.config.settings import settings


def create_app(testing=False):
    app = Flask(__name__)

    app.config.from_pyfile("config/settings.py")
    app.config.from_object(settings)
    app.logger.debug(app.config)

    api = Api(app)
    Swagger(app)

    if not testing:
        app.producer = KafkaProducer(
            bootstrap_servers=app.config['KAFKA_URL'],
            value_serializer=orjson.dumps,
            key_serializer=orjson.dumps
        )
        with app.app_context():
            create_topics(app)

    JWTManager(app)

    api.add_resource(Clicks, '/clicks/')
    api.add_resource(Pages, '/pages/')
    api.add_resource(Films, '/films/')
    api.add_resource(CustomEvents, '/custom_events/')

    @app.errorhandler(ValidationError)
    def register_validation_error(error):
        app.logger.error(error.messages)
        return error.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
