# fetch_comments.py
import logging

import threading
import time
import praw
from confluent_kafka import Producer
from datetime import datetime
from json import dumps
from data_collection.sentiment_analysis import analyze_sentiment

from config.praw_config import reddit  # Assuming your config is in praw_config.py

reddit = praw.Reddit(

)

threads = []
producer = Producer({"bootstrap.servers": "localhost:9092"})

class RedditProducer:

    def __init__(self, subreddit_list: list[str], reddit: praw.Reddit, producer):

        self.subreddit_list = subreddit_list
        self.reddit = reddit
        #self.comment_count = 0
        #self.start_time = time.time()
        self.log_file = "comment_log.txt"
        self.producer = producer

    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            logging.error(f"Message delivery failed: {err}")
        else:
            logging.info(f"Message delivered to {msg.topic()}")

    def log_to_file(self, message):
        with open(self.log_file, "a") as f:
            f.write(f"{message}\n")

    def start_streaming_threads(self):

        for subreddit_name in self.subreddit_list:
            thread = threading.Thread(target=self.start_stream, args=(subreddit_name,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def start_stream(self, subreddit_name) -> None:
        subreddit = self.reddit.subreddit(subreddit_name)
        comment: praw.models.Comment
        for comment in subreddit.stream.comments(skip_existing=True):
            #self.comment_count += 1

            #elapsed_time = time.time() - self.start_time
            #comments_per_second = self.comment_count / elapsed_time

            # Log metrics to the file
            #self.log_to_file(
            #    f"Total Comments: {self.comment_count}, Elapsed Time: {elapsed_time:.2f} seconds, Comments per Second: {comments_per_second:.2f}")

            # Optional: Limit the logging frequency

            try:
                comment_json = {
                    "id": comment.id,
                    "name": comment.name,
                    "author": comment.author.name,
                    "body": comment.body,
                    "subreddit": comment.subreddit.display_name,
                    "upvotes": comment.ups,
                    "downvotes": comment.downs,
                    "over_18": comment.over_18,
                    "timestamp": comment.created_utc,
                    "permalink": comment.permalink,
                }

                logging.info(f"subreddit: {subreddit_name}, comment: {comment_json}")
                self.producer.produce("reddit-comments", key=comment.id, value=dumps(comment_json),
                                      callback=self.delivery_report)
            except Exception as e:
                logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    subreddit_list = ['all']
    reddit_producer = RedditProducer(subreddit_list, reddit, producer)
    reddit_producer.start_streaming_threads()
