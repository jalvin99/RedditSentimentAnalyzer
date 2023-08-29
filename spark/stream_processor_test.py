from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StringType, StructType, StructField, IntegerType, BooleanType, FloatType

# Define the schema for the JSON value column
comment_schema = StructType([
    StructField("id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("author", StringType(), True),
    StructField("body", StringType(), True),
    StructField("subreddit", StringType(), True),
    StructField("upvotes", IntegerType(), True),
    StructField("downvotes", IntegerType(), True),
    StructField("over_18", BooleanType(), True),
    StructField("timestamp", FloatType(), True),
    StructField("permalink", StringType(), True),
])

spark: SparkSession = SparkSession.builder \
    .appName("StreamProcessor") \
    .getOrCreate()

# Kafka configurations
kafka_bootstrap_servers = "localhost:9092"
kafka_topic = "reddit-comments"

# Read from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

# Parse the value column as JSON
parsed_df = df.withColumn(
    "comment_json",
    from_json(df["value"].cast("string"), comment_schema)
)

output_df = parsed_df.select(
        "comment_json.id",
        "comment_json.name",
        "comment_json.author",
        "comment_json.body",
        "comment_json.subreddit",
        "comment_json.upvotes",
        "comment_json.downvotes",
        "comment_json.over_18",
        "comment_json.timestamp",
        "comment_json.permalink",
    )

# Microbatching for output_df - set processing time to 5 seconds
output_query = output_df.writeStream.trigger(processingTime="5 seconds") \
    .outputMode("append") \
    .format("console") \
    .start()

# Wait for any of the above queries to terminate
spark.streams.awaitAnyTermination()
