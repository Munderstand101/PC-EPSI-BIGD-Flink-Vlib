from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.datastream.stream_execution_environment import StreamExecutionEnvironment
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.datastream.window import TumblingProcessingTimeWindows
from pyflink.common import WatermarkStrategy, Time
from pyflink.common.typeinfo import Types

env = StreamExecutionEnvironment.get_execution_environment()
env.add_jars('file:///home/ubuntu/exemple/flink-sql-connector-kafka-1.17.2.jar')

source = KafkaSource.builder() \
    .set_bootstrap_servers("localhost:9092") \
    .set_topics("triplets") \
    .set_group_id("triplets-flink") \
    .set_starting_offsets(KafkaOffsetsInitializer.latest()) \
    .set_value_only_deserializer(
        JsonRowDeserializationSchema.builder().type_info(Types.ROW_NAMED(
            [ 'cle', 'val0', 'val1', 'val2'], 
            [ Types.STRING(), Types.INT(), Types.INT(), Types.INT()])).build()
    ) \
    .build()

stream = env.from_source(source, WatermarkStrategy.no_watermarks(), "triplets")

stream .map(lambda ligne : (ligne[0], f"{ligne[3]}", 1), output_type=Types.TUPLE([Types.STRING(), Types.STRING(), Types.INT()])) \
    .key_by(lambda ligne : ligne[0]) \
    .window(TumblingProcessingTimeWindows.of(Time.seconds(10))) \
    .reduce(lambda a, b: (a[0], f"{a[1]} {b[1]}", a[2]+b[2])) \
    .print()

env.execute()
