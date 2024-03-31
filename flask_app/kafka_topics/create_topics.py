from enum import StrEnum

from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError


class Topics(StrEnum):
    CLICKS = 'clicks'
    CUSTOM_EVENTS = 'custom_events'
    VIEWS = 'views'
    PAGES = 'pages'



def create_topics():
    from app import app

    admin_client = KafkaAdminClient(
        bootstrap_servers=app.config['KAFKA_URL'],
    )
    topic_list = list()

    for name in Topics:
        topic_list.append(NewTopic(
            name=name,
            num_partitions=app.config['KAFKA_NUM_PARTITIONS'],
            replication_factor=app.config['KAFKA_REPLICATION_FACTOR'],
            topic_configs={
                'retention.ms': app.config['KAFKA_RETENTION_MS'],
                'min.insync.replicas': app.config['KAFKA_MIN_INSYNC_REPLICAS']
            }
        ))

    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except TopicAlreadyExistsError:
        pass
