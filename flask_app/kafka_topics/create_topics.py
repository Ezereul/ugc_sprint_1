from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError


def create_topics():
    from app import app

    admin_client = KafkaAdminClient(
        bootstrap_servers=app.config['KAFKA_URL'],
    )
    topic_list = list()
    topic_names = ['clicks', 'custom_events', 'views', 'pages']

    for name in topic_names:
        topic_list.append(NewTopic(name=name, num_partitions=3, replication_factor=3,
                                   topic_configs={'retention.ms': '86400000',
                                                  'min.insync.replicas': '2'}))

    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except TopicAlreadyExistsError:
        pass
