import psycopg2
from psycopg2 import sql
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv("dbconfig.env")

# initializing db connection through env variables
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

def write_to_db(comment):
    # converting unix timestamp into PostgreSQL compliant timestamp form
    comment_timestamp = datetime.fromtimestamp(comment['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

    insert_query = sql.SQL(
        "INSERT INTO reddit_comments (id, name, author, body, subreddit, upvotes, downvotes, over_18, timestamp, permalink, sentiment_score, anger, anticip, disgust, fear, joy, negative, positive, sadness, surprise, trust) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    cursor.execute(insert_query, (
        comment['id'], comment['name'], comment['author'], comment['body'],
        comment['subreddit'], comment['upvotes'], comment['downvotes'],
        comment['over_18'], comment_timestamp, comment['permalink'],
        comment['sentiment_score'], comment['anger'], comment['anticip'],
        comment['disgust'], comment['fear'], comment['joy'], comment['negative'],
        comment['positive'], comment['sadness'], comment['surprise'], comment['trust']
    ))

    conn.commit()

if __name__ == "__main__":
    from fetch_comments import fetch_comments
    subreddit_list = ['all']
    for comment in fetch_comments(subreddit_list):
        write_to_db(comment)
