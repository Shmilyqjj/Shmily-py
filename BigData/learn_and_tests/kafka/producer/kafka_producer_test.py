#!/usr/bin/env python
# encoding: utf-8
"""
:Description: Kafka python生产者
:Author: 佳境Shmily
:Create Time: 2021/11/25 20:49
:File: kafka_producer_test
:Site: shmily-qjj.top
:需要安装的包
pip install kafka
pip install kafka-python
"""

from kafka import KafkaProducer
import time
from kafka.errors import kafka_errors

# 查看当前有哪些topic：
# kafka-topics --list --bootstrap-server 192.168.1.101:9092,192.168.1.102:9092,192.168.1.103:9092,192.168.1.104:9092

# 创建测试topic
# kafka-topics --create --zookeeper 192.168.1.101:2181 --replication-factor 3 --partitions 1 --topic test_topic


BOOTSTRAP_SERVERS = '192.168.1.101:9092,192.168.1.102:9092,192.168.1.103:9092,192.168.1.104:9092'
TOPIC = 'test_topic'


def send_kafka_method1():
    """
    发送方式一
    发送并忘记（不关注是否正常到达，不对返回结果做处理）
    :return:
    """
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    start_time = time.time()
    for i in range(0, 10000):
        msg = 'echo %s' % i
        # print(msg)
        future = producer.send(TOPIC, msg.encode(), partition=0)
    # 将缓冲区的全部消息push到broker当中
    producer.flush()
    producer.close()
    time_cost = time.time() - start_time
    print('发送耗时 %s 秒' % time_cost)


def send_kafka_method2():
    """
    发送方式二
    同步发送(通过get方法等待Kafka的响应，判断消息是否发送成功)
    :return:
    """
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    start_time = time.time()
    for i in range(0, 10):
        msg = 'echo %s' % i
        # print(msg)
        future = producer.send(TOPIC, msg.encode(), partition=0)
        # 同步阻塞,通过调用get()方法进而保证一定程序是有序的.
        try:
            record_metadata = future.get(timeout=10)
            print('topic:%s partition:%s offset:%s 消息 %s 发送成功' % (record_metadata.topic, record_metadata.partition, record_metadata.offset, msg))
        except kafka_errors as e:
            print(str(e))
    producer.close()
    time_cost = time.time() - start_time
    print('发送耗时 %s 秒' % time_cost)


def send_kafka_method3():
    """
    异步发送+回调函数(消息以异步的方式发送，通过回调函数返回消息发送成功/失败)
    :return:
    """
    on_send_success = lambda x: f"send success {x}"
    on_send_error = lambda x: f"send error {x}"
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    start_time = time.time()
    for i in range(0, 10000):
        msg = 'echo %s' % i
        # print(msg)
        # 如果成功,传进record_metadata,如果失败,传进Exception.
        producer.send(
            topic=TOPIC, value=msg.encode(), partition=0
        ).add_callback(on_send_success).add_errback(on_send_error)

    producer.flush()
    producer.close()

    time_cost = time.time() - start_time
    print('发送耗时 %s 秒' % time_cost)

if __name__ == '__main__':
    send_kafka_method1()
    # send_kafka_method2()
    send_kafka_method3()