import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json, col, from_unixtime, avg, current_timestamp
from pyspark.sql.types import StringType, StructType, StructField, IntegerType, BooleanType, FloatType, TimestampType
import uuid

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']

sentiment_udf = udf(analyze_sentiment, FloatType())

def make_uuid():
    return str(uuid.uuid1())

make_uuid_udf = udf(make_uuid, StringType())

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
    .config("spark.jars", "C:/spark-3.4.1-bin-hadoop3/jars/postgres-42.6.0.jar") \
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
    ) \
    .withColumn("uuid", make_uuid_udf()) \
    .withColumn("api_timestamp", from_unixtime(col("timestamp").cast("int")).cast(TimestampType())) \
    .withColumn("ingest_timestamp", current_timestamp()) \
    .drop("timestamp")

# Adding sentiment score
output_df = output_df.withColumn(
    'sentiment_score', sentiment_udf(output_df['body'])
)

# Microbatching for output_df - set processing time to 5 seconds
output_query = output_df.writeStream.trigger(processingTime="5 seconds") \
    .foreachBatch(
        lambda batchDF, batchID: batchDF.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://localhost/postgres") \
            .option("dbtable", "comments3") \
            .option("user", "postgres") \
            .option("password", "") \
            .mode("append") \
            .save()
    ).outputMode("append").start()

# Adding moving averages in another df
summary_df = output_df.withWatermark("ingest_timestamp", "1 minute").groupBy("subreddit") \
    .agg(avg("sentiment_score").alias("sentiment_score_avg")) \
    .withColumn("uuid", make_uuid_udf()) \
    .withColumn("ingest_timestamp", current_timestamp())

# Microbatching for summary_df - set processing time to 5 seconds
summary_query = summary_df.writeStream.trigger(processingTime="5 seconds") \
    .foreachBatch(
        lambda batchDF, batchID: batchDF.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://localhost/postgres") \
            .option("dbtable", "subreddit_sentiment_avg3") \
            .option("user", "postgres") \
            .option("password", "") \
            .mode("append").save()
    ).outputMode("update").start()

# Wait for any of the above queries to terminate
spark.streams.awaitAnyTermination()