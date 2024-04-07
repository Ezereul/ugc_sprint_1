#!/bin/bash

wait_for_kafka_cluster() {
    for kafka_host in "${KAFKA_1_HOST}:${KAFKA_1_PORT}" "${KAFKA_2_HOST}:${KAFKA_2_PORT}" "${KAFKA_3_HOST}:${KAFKA_3_PORT}"; do
        IFS=: read host port <<< $kafka_host
        echo "Проверка доступности Kafka на $host порт $port..."
        until nc -z $host $port; do
            echo "Ожидание доступности Kafka на $host порт $port..."
            sleep 1
        done
    done
    echo "Все узлы Kafka доступны."
}

wait_for_clickhouse_cluster() {
    for clickhouse_host in "${CLICKHOUSE_1_HOST}:${CLICKHOUSE_1_PORT}" \
                           "${CLICKHOUSE_2_HOST}:${CLICKHOUSE_2_PORT}" \
                           "${CLICKHOUSE_3_HOST}:${CLICKHOUSE_3_PORT}" \
                           "${CLICKHOUSE_4_HOST}:${CLICKHOUSE_4_PORT}"; do
        IFS=: read host port <<< $clickhouse_host
        echo "Проверка доступности ClickHouse на $host порт $port..."
        until curl -s "http://${host}:${port}" > /dev/null; do
            echo "Ожидание доступности ClickHouse на $host порт $port..."
            sleep 1
        done
    done
    echo "Все узлы ClickHouse доступны."
}

wait_for_kafka_cluster

wait_for_clickhouse_cluster

echo "Создание таблиц..."
python src/components/loader.py

echo "Запуск ETL процесса..."
python main.py
