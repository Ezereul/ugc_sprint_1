import orjson
from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from kafka import KafkaProducer

from api.v1.clicks import Clicks
from api.v1.custom_events import CustomEvents
from api.v1.films import Films
from api.v1.pages import Pages
from kafka_topics.create_topics import create_topics

app = Flask(__name__)

api = Api(app)
swagger = Swagger(app)
app.config.from_pyfile("config/settings.py")

producer = KafkaProducer(bootstrap_servers=app.config['KAFKA_URL'],
                         value_serializer=orjson.dumps,
                         key_serializer=orjson.dumps)

jwt = JWTManager(app)

api.add_resource(Clicks, '/clicks/')
api.add_resource(Pages, '/pages/')
api.add_resource(Films, '/films/')
api.add_resource(CustomEvents, '/custom_events/')

create_topics()


if __name__ == '__main__':

    app.run()
