#!/bin/bash
# 执行分区重新分配

ZK=zk_ip:2181/kafka-1.1.1
THROTTLE=524288000
KAFKA_HOME=/usr/local/complat/kafka

$KAFKA_HOME/bin/kafka-reassign-partitions.sh --zookeeper $ZK --execute --reassignment-json-file reassign.json —-throttle $THPOTTLE