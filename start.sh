#!/bin/bash

KAFKA_PREFIX=2.13
KAFKA_VERSION=3.6.1
KAFKA_FULL_VERSION=$KAFKA_PREFIX-$KAFKA_VERSION
KAFKA_PATH=~/kafka_$KAFKA_FULL_VERSION

FLINK_VERSION=1.18.1
FLINK_SCALA_VERSION=2.12

PATH=$PATH:$KAFKA_PATH/bin:~/flink-$FLINK_VERSION/bin

export PATH

kafka-server-start.sh $KAFKA_PATH/config/kraft/server.properties > /dev/null &
start-cluster.sh

echo "Type : PATH=\$PATH:$KAFKA_PATH/bin:~/flink-$FLINK_VERSION/bin"
