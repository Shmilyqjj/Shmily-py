#!/bin/bash

ZK=zk_ip:2181/kafka-1.1.1
BROKERS=broker1:9092,broker2:9092,broker3:9092,broker4:9092,broker5:9092,broker6:9092,broker7:9092,broker8:9092
BROKERIDS=0,1,2,3,4,5,6,7,9,10,11,12,13,14,16,17,18
KAFKA_HOME=/usr/local/complat/kafka

$KAFKA_HOME/bin/kafka-reassign-partitions.sh --zookeeper $ZK --broker-list "$BROKERIDS" --topics-to-move-json-file reassign_generate.json --generate > generate.json

echo "========Generated json file: generate.json========"

cat generate.json

echo "========Generated json file: generate.json========"