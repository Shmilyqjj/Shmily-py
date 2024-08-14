#!/usr/bin/env python
# encoding: utf-8
"""
:Description: Kafka python生产者 (轮询分区发送)
:Author: 佳境Shmily
:Create Time: 2023/12/25 20:49
:File: kafka_producer_test
:Site: shmily-qjj.top
:需要安装的包
pip install kafka
pip install kafka-python
"""
import time
from kafka import KafkaProducer
from kafka import KafkaAdminClient


def send_kafka(bootstraps: str, topic: str, msg: str, send_row_cnt: int, partition: int):
    admin = KafkaAdminClient(bootstrap_servers=bootstraps)
    producer = KafkaProducer(bootstrap_servers=bootstraps)
    partition_cnt = len(admin.describe_topics(topics=[topic])[0].get('partitions'))
    start_time = time.time()

    for i in range(0, send_row_cnt):
        partition_id = partition if partition >= 0 else i % partition_cnt
        if msg != '':
            producer.send(topic, msg.encode(), partition=partition_id)
        else:
            sent_msg = '''{"id": %d, "partition_id": %d}''' % (i, partition_id)
            producer.send(topic, sent_msg.encode(), partition=partition_id)

    # 将缓冲区的全部消息push到broker当中
    producer.flush()
    producer.close()

    print('发送耗时 %s 秒' % (time.time() - start_time))


if __name__ == '__main__':
    bootstrap_servers = "localhost:9092"
    topic = "qjj"
    message = '''{"a": "b", "c": "d", "e": 1}'''
    # send_kafka(bootstrap_servers, topic, '', 10100, -1)
    send_kafka(bootstrap_servers,
               topic,
               '{"@event_name":"haha","@event_time": "2024-06-20 21:19:43", "@ip": "127.0.0.1","@dt": "2024-06-20 21:19:43"}',
               1000000, -1)

    # send_kafka(bootstrap_servers, topic, '', 1, 0)
    # send_kafka(bootstrap_servers, topic, '', 6372, 1)
    # send_kafka(bootstrap_servers, topic, '', 8372, 2)
    # send_kafka(bootstrap_servers, topic, '', 12872, 3)