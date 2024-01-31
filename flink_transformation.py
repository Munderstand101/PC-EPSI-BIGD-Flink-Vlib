from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.datastream.window import TumblingProcessingTimeWindows
from pyflink.common import WatermarkStrategy, Time
from pyflink.common.typeinfo import Types
from pyflink.datastream.functions import CoProcessFunction

env = StreamExecutionEnvironment.get_execution_environment()
env.add_jars('file:///home/munderstand/flink_vlib/flink-sql-connector-kafka-3.0.2-1.18.jar')

source_docks = KafkaSource.builder() \
    .set_bootstrap_servers("localhost:9092") \
    .set_topics("bornette_libre_par_station") \
    .set_group_id("docks-flink") \
    .set_starting_offsets(KafkaOffsetsInitializer.latest()) \
    .set_value_only_deserializer(
        JsonRowDeserializationSchema.builder().type_info(Types.ROW_NAMED(
            ['station_id', 'num_docks_available'], 
            [Types.STRING(), Types.INT()])).build()
    ) \
    .build()

source_bikes = KafkaSource.builder() \
    .set_bootstrap_servers("localhost:9092") \
    .set_topics("velo_disponibilite_par_station") \
    .set_group_id("velo_station_group") \
    .set_starting_offsets(KafkaOffsetsInitializer.latest()) \
    .set_value_only_deserializer(
        JsonRowDeserializationSchema.builder().type_info(Types.ROW_NAMED(
            ['station_id', 'bikes_available'], 
            [Types.STRING(), Types.INT()])).build()
    ) \
    .build()

stream_docks = env.from_source(source_docks, WatermarkStrategy.no_watermarks(), "docks")
stream_bikes = env.from_source(source_bikes, WatermarkStrategy.no_watermarks(), "bikes")

connected_stream = stream_docks.connect(stream_bikes)

class JoinFunction(CoProcessFunction):
    def open(self, runtime_context):
        bikes_state_descriptor = Types.ROW_NAMED(
            ['station_id', 'bikes_available'], 
            [Types.STRING(), Types.INT()])
        self.bikes_state = runtime_context.get_broadcast_state(bikes_state_descriptor)
        
    def process_element1(self, value, ctx, out):
        if value[0] in self.bikes_state:
            bikes_value = self.bikes_state.get(value[0])
            out.collect((value[0], f"Average docks: {value[1]}, Average bikes: {bikes_value[1]}", 1))

    def process_element2(self, value, ctx, out):
        self.bikes_state.put(value[0], value[1])

result_stream = connected_stream.process(JoinFunction())

result_stream.print()

print("Executing the job...")
try:
    env.execute()
    print("Job executed successfully.")
except Exception as e:
    print("Error executing the job:", e)
    e.printStackTrace()
