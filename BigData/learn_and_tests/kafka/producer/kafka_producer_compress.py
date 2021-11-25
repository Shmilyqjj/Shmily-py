#!/usr/bin/env python
# encoding: utf-8
"""
:Description: Kafka生产者发送压缩数据流
:Author: 佳境Shmily
:Create Time: 2021/11/25 21:44
:File: kafka_producer_compress
:Site: shmily-qjj.top
"""
import gzip



from kafka import KafkaProducer
import time
from kafka.errors import kafka_errors
import io

BOOTSTRAP_SERVERS = '192.168.1.101:9092,192.168.1.102:9092,192.168.1.103:9092,192.168.1.104:9092'
TOPIC = 'test_topic'


def gzip_compress(msg_str):
    try:
        buf = io.BytesIO()
        with gzip.GzipFile(mode='wb', fileobj=buf) as f:
            f.write(msg_str)
        return buf.getvalue()
    except BaseException as e:
        print("Gzip解压错误 %s" % str(e))


def gzip_uncompress(c_data):
    try:
        buf = io.BytesIO(c_data)
        with gzip.GzipFile(mode='rb', fileobj=buf) as f:
            return f.read()
    except BaseException as e:
        print("Gzip解压错误 %s" % str(e))


def send_compressed_data_to_kafka(topic_name, msg, key=None):
    if key is not None:
        producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS,
                                 key_serializer=gzip_compress, value_serializer=gzip_compress)
        r = producer.send(topic_name, value=msg, key=key)
    else:
        producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS,
                                 value_serializer=gzip_compress)
        r = producer.send(topic_name, value=str.encode(msg, 'utf-8'))
    producer.close(timeout=5)
    return r.get()


if __name__ == '__main__':
    # x = gzip_compress('qjj'.encode())
    # print(gzip_uncompress(x))
    print(send_compressed_data_to_kafka(TOPIC, "qjj"))
    print(send_compressed_data_to_kafka(TOPIC, "abc"))

