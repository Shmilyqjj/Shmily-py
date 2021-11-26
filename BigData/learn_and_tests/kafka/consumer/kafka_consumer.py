#!/usr/bin/env python
# encoding: utf-8
"""
:Description: kafka消费
:Author: 佳境Shmily
:Create Time: 2021/11/26 20:26
:File: kafka_consumer
:Site: shmily-qjj.top
"""
from kafka import KafkaConsumer, TopicPartition
import time

BOOTSTRAP_SERVERS = '192.168.1.101:9092,192.168.1.102:9092,192.168.1.103:9092,192.168.1.104:9092'
TOPIC = 'test_topic'


def consume_demo():
    """
    普通demo 无高级参数
    :return:
    """
    consumer = KafkaConsumer(TOPIC,bootstrap_servers=BOOTSTRAP_SERVERS)
    for message in consumer:
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))


def consume_consumer_group():
    consumer = KafkaConsumer(TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS, group_id='my-group')
    for message in consumer:
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))


def consume_earliest_data():
    """
    auto_offset_reset消费自定义偏移量的数据
     {'smallest': 'earliest', 'largest': 'latest'}
    :return:
    """
    # auto_offset_reset: 重置偏移量，earliest移到最早的可用消息，latest最新的消息，默认为latest
    consumer = KafkaConsumer(TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS, auto_offset_reset='earliest')
    for message in consumer:
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))


def offset_manage_manually_consume():
    """
    手动设置offset
    :return:
    """
    consumer = KafkaConsumer(TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS)
    print(consumer.partitions_for_topic(TOPIC))  # 获取topic的分区信息
    print(consumer.topics())  # 获取topic列表  当前kafka server有哪些topic
    print(consumer.subscription())  # 获取当前消费者订阅的topic
    print(consumer.assignment())  # 获取当前消费者topic、分区信息
    print(consumer.beginning_offsets(consumer.assignment()))  # 获取当前消费者可消费的偏移量
    print(consumer.assignment())  # 获取当前消费者可消费的偏移量
    consumer.seek(TopicPartition(topic=u'%s' % TOPIC, partition=0), 235000)  # 重置偏移量，从第235000个偏移量消费
    for message in consumer:
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))


def subscribe_multiple_topics():
    """
    订阅多个主题
    :return:
    """
    consumer = KafkaConsumer(TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS)
    consumer.subscribe(topics=[TOPIC, 'flumeTopic']) # 订阅要消费的主题
    print(consumer.topics())
    print(consumer.position(TopicPartition(topic=u'%s' % TOPIC, partition=0)))  # 获取当前topic的最新偏移量
    for message in consumer:
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                              message.offset, message.key,
                                              message.value))


def manually_pull_data():
    """
    手动拉取消息
    :return:
    """
    consumer = KafkaConsumer(TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS)
    while True:
        msg = consumer.poll(timeout_ms=5)  # 从kafka获取消息
        print(msg)
        time.sleep(0.001)


def message_hangup_recovery():
    """
    消息挂起与恢复
    :return:
    """
    consumer = KafkaConsumer(TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS)
    consumer.subscribe(topics=[TOPIC])
    consumer.topics()
    consumer.pause(TopicPartition(topic=u'%s' % TOPIC, partition=0))
    num = 0
    while True:
        print(num)
        # pause执行后，consumer不能读取，直到调用resume后恢复
        print(consumer.paused())  # 获取当前挂起的消费者
        msg = consumer.poll(timeout_ms=5)
        print(msg)
        time.sleep(2)
        num = num + 1
        if num == 10:
            print("resume...")
            consumer.resume(TopicPartition(topic=u'test', partition=0))
            print("resume......")


if __name__ == '__main__':
    # consume_demo()
    # consume_consumer_group()
    # consume_earliest_data()
    # offset_manage_manually_consume()
    # subscribe_multiple_topics()
    # manually_pull_data()
    message_hangup_recovery()
