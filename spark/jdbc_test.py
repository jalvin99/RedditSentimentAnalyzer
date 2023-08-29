from pyspark.sql import SparkSession
from datetime import datetime

# Initialize Spark session
spark = SparkSession.builder \
    .appName("PostgresConnectionTest") \
    .config("spark.jars", "C:/spark-3.4.1-bin-hadoop3/jars/postgres-42.6.0.jar") \
    .getOrCreate()

# Sample data for 'comments3' table
comments_data = [("1", "name1", "author1", "body1", "subreddit1", 5, 0, True, "permalink1", datetime.strptime('2023-08-28 12:34:56', '%Y-%m-%d %H:%M:%S'), datetime.strptime('2023-08-28 12:35:56', '%Y-%m-%d %H:%M:%S'), "uuid1", 0.5)]
comments_columns = ["id", "name", "author", "body", "subreddit", "upvotes", "downvotes", "over_18", "permalink", "api_timestamp", "ingest_timestamp", "uuid", "sentiment_score"]
comments_df = spark.createDataFrame(comments_data, comments_columns)

# Sample data for 'subreddit_sentiment_avg3' table
subreddit_data = [("subreddit1", 0.5, "uuid2", datetime.strptime('2023-08-28 12:36:56', '%Y-%m-%d %H:%M:%S'))]
subreddit_columns = ["subreddit", "sentiment_score_avg", "uuid", "ingest_timestamp"]
subreddit_df = spark.createDataFrame(subreddit_data, subreddit_columns)

# Connection details
jdbc_url = "jdbc:postgresql://localhost/postgres"
connection_properties = {
    "user": "postgres",
    "password": "",
    "driver": "org.postgresql.Driver"
}

# Write sample data to 'comments3' table
comments_df.write \
    .jdbc(jdbc_url, "comments3", mode="append", properties=connection_properties)

# Write sample data to 'subreddit_sentiment_avg3' table
subreddit_df.write \
    .jdbc(jdbc_url, "subreddit_sentiment_avg3", mode="append", properties=connection_properties)

print("Sample data written to PostgreSQL tables.")

# Stop the Spark session
spark.stop()
