from flasgger import Schema

from kafka_topics.send import send_message


class BaseService:
    schema: Schema = None
    topic: str = None

    def send(self, user_id: str, args: dict):
        args['user_id'] = user_id

        user_event = self.schema.load(args)

        send_message(self.topic, user_event['user_id'], user_event)
