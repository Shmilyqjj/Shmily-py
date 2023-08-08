#!/usr/bin/env python
# encoding: utf-8
"""
: 给定topic partition数 replication数 brokerIds 生成均匀不倾斜的kafka分区重新分配脚本 供kafka-reassign-partitions.sh脚本调用
:Author: shmily
:Create Time: 2023/8/8 下午3:02
:@File: generate_reassign_file.py.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""
import json

TOPIC_NAME = "t_rcv4"
BROKERS = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 16, 17, 18]
PARTITION_NUM = 64
REPLICA_NUM = 3

data = {"version": 1, "partitions": []}
broker_num = len(BROKERS)
for partition_id in range(PARTITION_NUM):
    leader_idx = partition_id % broker_num
    leader_broker_id = BROKERS[leader_idx]
    replicas = [leader_broker_id]
    if REPLICA_NUM != 1:
        for i in range(1, REPLICA_NUM):
            if leader_idx + i <= broker_num - 1:
                follower_broker_id = BROKERS[leader_idx + i]
            else:
                follower_broker_id = BROKERS[leader_idx + i - broker_num]
            replicas.append(follower_broker_id)
    log_dirs = ["any" for i in range(REPLICA_NUM)]
    partition = {"topic": TOPIC_NAME, "partition": partition_id, "replicas": replicas, "log_dirs": log_dirs}
    print(partition)
    data["partitions"].append(partition)

print(json.dumps(data))
