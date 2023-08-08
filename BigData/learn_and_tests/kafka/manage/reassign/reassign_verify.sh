#!/bin/bash
# 查看分区重新分配任务进度，状态

ZK=zk_ip:2181/kafka-1.1.1
KAFKA_HOME=/usr/local/complat/kafka
$KAFKA_HOME/bin/kafka-reassign-partitions.sh --zookeeper $ZK --verify --reassignment-json-file reassign.json