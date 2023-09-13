from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType, IntegerType, BooleanType, LongType, FloatType, \
    ArrayType
from pyspark.sql.functions import udf, from_json, col
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nrclex import NRCLex
import nltk
from statistics import mean


def analyze_sentiment_vader(text):
    vader_analyzer = SentimentIntensityAnalyzer()
    sentences = nltk.sent_tokenize(text)
    scores = {'neg': [], 'neu': [], 'pos': [], 'compound': []}

    for sentence in sentences:
        sentiment = vader_analyzer.polarity_scores(sentence)
        for key in scores.keys():
            scores[key].append(sentiment[key])

    avg_scores = {key: mean(scores[key]) for key in scores.keys()}
    return [avg_scores['neg'], avg_scores['neu'], avg_scores['pos'], avg_scores['compound']]


def analyze_emotion_nrc(text):
    sentences = nltk.sent_tokenize(text)
    emotions_sum = {'anger': 0, 'anticip': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'negative': 0, 'positive': 0,
                    'sadness': 0, 'surprise': 0, 'trust': 0}

    for sentence in sentences:
        emotion = NRCLex(sentence).affect_frequencies
        for key in emotions_sum.keys():
            if key in emotion:
                emotions_sum[key] += emotion[key]

    num_sentences = len(sentences)
    avg_emotions = {key: emotions_sum[key] / num_sentences for key in emotions_sum.keys()}
    return avg_emotions

def main():
    nltk.download('vader_lexicon')

    sentiment_udf = udf(analyze_sentiment_vader, ArrayType(FloatType()))
    emotion_udf = udf(analyze_emotion_nrc, ArrayType(FloatType()))

    # Initialize Spark
    spark = SparkSession.builder \
        .appName("Reddit Comment Processor") \
        .getOrCreate()

    comment_schema = StructType([
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("author", StringType(), True),
        StructField("body", StringType(), True),
        StructField("subreddit", StringType(), True),
        StructField("upvotes", IntegerType(), True),
        StructField("downvotes", IntegerType(), True),
        StructField("over_18", BooleanType(), True),
        StructField("timestamp", LongType(), True),
        StructField("permalink", StringType(), True)
    ])

    raw_stream = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "reddit-comments") \
        .load()

    parsed_df = raw_stream.selectExpr("CAST(value AS STRING)")
    parsed_df = parsed_df.withColumn("value", from_json("value", comment_schema)).select("value.*")
    parsed_df = parsed_df.withColumn("sentiment_values", sentiment_udf("body"))
    parsed_df = parsed_df.withColumn("emotion_values", emotion_udf("body"))

    output_df = parsed_df.select(
        "id",
        "name",
        "author",
        "body",
        "subreddit",
        "upvotes",
        "downvotes",
        "over_18",
        "timestamp",
        "permalink",
        col("sentiment_values")[0].alias("VADER_neg"),
        col("sentiment_values")[1].alias("VADER_neu"),
        col("sentiment_values")[2].alias("VADER_pos"),
        col("sentiment_values")[3].alias("sentiment_score"),
        col("emotion_values")[0].alias("NRC_anger"),
        col("emotion_values")[1].alias("NRC_anticipation"),
        col("emotion_values")[2].alias("NRC_disgust"),
        col("emotion_values")[3].alias("NRC_fear"),
        col("emotion_values")[4].alias("NRC_joy"),
        col("emotion_values")[5].alias("NRC_negative"),
        col("emotion_values")[6].alias("NRC_positive"),
        col("emotion_values")[7].alias("NRC_sadness"),
        col("emotion_values")[8].alias("NRC_surprise"),
        col("emotion_values")[9].alias("NRC_trust")
    )

    output_query = output_df \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    output_query.awaitTermination()


if __name__ == "__main__":
    main()
