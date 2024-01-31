#!/bin/bash

KAFKA_PREFIX=2.13
KAFKA_VERSION=3.6.1
KAFKA_FULL_VERSION=$KAFKA_PREFIX-$KAFKA_VERSION

FLINK_VERSION=1.18.1
FLINK_SCALA_VERSION=2.12

apt update -y
apt install -y default-jre python3-pip python3-venv python3-wheel

ln /bin/python3 /bin/python

cd ~

wget https://dlcdn.apache.org/kafka/$KAFKA_VERSION/kafka_$KAFKA_FULL_VERSION.tgz
tar -xzf kafka_$KAFKA_FULL_VERSION.tgz

wget https://dlcdn.apache.org/flink/flink-$FLINK_VERSION/flink-$FLINK_VERSION-bin-scala_$FLINK_SCALA_VERSION.tgz
tar -xzf flink_$FLINK_VERSION-bin-scala_$FLINK_SCALA_VERSION.tgz

sed -i 's/rest.bind-address: localhost/rest.bind-address: 0.0.0.0/g' flink-$FLINK_VERSION/conf/flink-conf.yaml

cd kafka_$KAFKA_FULL_VERSION

KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
